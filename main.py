from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from pydantic import BaseModel
from datetime import datetime, timedelta
from PIL import Image
import numpy as np
import io
import boto3
from botocore.exceptions import NoCredentialsError
from boto3 import resource
from botocore.exceptions import ClientError
import os
from fastapi import Form
from boto3.dynamodb.conditions import Key

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# --- Config ---
SECRET_KEY = "mysecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# DynamoDB client
dynamodb = resource("dynamodb", region_name="ap-southeast-2")
table = dynamodb.Table("n11375370-ascii-db")  # ✅ Correct shared table


# --- Fake DB ---
users_db = {
    "admin": {
        "username": "admin",
        "password": "$2b$12$5BKfCNb9QgoVQeKci6/TFOPxXizkERxxJoMCoZB4C1eutgv8qKtwO"  # admin123
    },
    "bob": {
        "username": "bob",
        "password": "$2b$12$5BKfCNb9QgoVQeKci6/TFOPxXizkERxxJoMCoZB4C1eutgv8qKtwO"  # admin123
    }
}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Models ---
class LoginForm(BaseModel):
    username: str
    password: str

# --- Helpers ---
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username not in users_db:
            raise HTTPException(status_code=401, detail="Invalid user")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# --- Routes ---

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    user = users_db.get(username)
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": username})
    return {"access_token": token}


@app.post("/convert")
async def convert_image(
    file: UploadFile = File(...),
    username: str = Depends(get_current_user)
):
    contents = await file.read()

    try:
        image = Image.open(io.BytesIO(contents)).convert("L")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    image = image.resize((100, 50))
    chars = "@%#*+=-:. "
    ascii_art = ""
    arr = np.array(image)

    for row in arr:
        ascii_art += "".join([chars[min(pixel // 25, 9)] for pixel in row]) + "\n"

    # Save ASCII art to local file
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    filename = f"{username}_{timestamp}.txt"
    local_path = f"/tmp/{filename}"
    with open(local_path, "w") as f:
        f.write(ascii_art)

    # Upload to S3 with presigned URL
    bucket_name = "ascii-api-video-store"
    s3_key = f"ascii_output/{filename}"
    presigned_url = upload_to_s3(local_path, bucket_name, s3_key)
    if not presigned_url:
        raise HTTPException(status_code=500, detail="S3 upload failed")

    # Save metadata
    try:
        table.put_item(
            Item={
                "qut-username": username,  # partition key
                "filename": file.filename,  # sort key
                "timestamp": datetime.utcnow().isoformat(),
                "s3_key": s3_key,
                "size": f"{image.size[0]}x{image.size[1]}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DynamoDB Error: {str(e)}")



    # Return result with preview + secure download link
    return {
        "message": "Image converted and uploaded successfully.",
        "ascii_preview": ascii_art[:1000],
        "s3_key": s3_key,
        "download_url": presigned_url
    }



@app.get("/results")
def get_metadata(username: str = Depends(get_current_user)):
    table = boto3.resource("dynamodb", region_name="ap-southeast-2").Table("AsciiMetadata")

    try:
        response = table.query(
            KeyConditionExpression=Key("qut-username").eq(f"{username}")
        )
        items = response.get("Items", [])
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/healthz")
def health_check():
    return {"status": "ok"}

#--- S3 Function ---
def upload_to_s3(file_path, bucket_name, s3_key):
    s3 = boto3.client('s3')
    try:
        # Upload as private (default)
        s3.upload_file(
            file_path,
            bucket_name,
            s3_key,
            ExtraArgs={'ACL': 'private'}
        )

        # Generate presigned URL (valid 15 minutes)
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': s3_key},
            ExpiresIn=900  # 15 minutes
        )

        return presigned_url
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return None


