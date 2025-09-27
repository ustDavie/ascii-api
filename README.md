# ascii-api
dmdmdmd
# ASCII Image API - Assignment 2 (CAB432)

## ✅ What’s Done

- [x] FastAPI app set up and running locally
- [x] `/login` endpoint implemented with JWT authentication
- [x] `/convert` endpoint working:
  - Uploads image
  - Converts to ASCII
  - Saves output `.txt` file locally
  - Uploads ASCII `.txt` to S3 bucket
  - ✅ Preview included in response
- [x] S3 bucket set up and connected (ascii-api-video-store)
- [x] Swagger docs working at `/docs`
- [x] Authentication works with Bearer token in Swagger
- [x] User’s ASCII file stored using timestamp-based naming

## ❌ What Still Needs Work

- [ ] DynamoDB metadata save:
  - Table exists (`AsciiMetadata`)
  - Getting `AccessDeniedException` on `PutItem`
  - Needs IAM permissions or SSO role fix
- [ ] Confirm read/query from DynamoDB is working (optional)
- [ ] Error handling improvements (optional)
- [ ] Styling or UI (optional)

# ASCII Image API - Assignment 2 (CAB432)

## ✅ What’s Done So Far (by [Your Name])

- [x] FastAPI app set up and running locally
- [x] `/login` endpoint implemented with JWT authentication (2 users: `admin`, `bob`)
- [x] `/convert` endpoint working:
  - Uploads image
  - Converts to ASCII
  - Saves ASCII art as `.txt` locally
  - Uploads output file to S3 bucket (`ascii-api-video-store`)
  - Returns preview + download URL
- [x] S3 bucket created and working
- [x] Swagger UI works at `/docs` (with token auth)
- [x] ASCII output file is uniquely named using timestamp

---

## ❌ What Still Needs Work (To-Do)

### 🔴 DynamoDB

- [ ] Fix DynamoDB `PutItem` error (permissions issue)
- [ ] Ensure table `AsciiMetadata` exists with:
  - Partition key: `qut-username` (String)
  - Sort key: `timestamp` (String)
- [ ] Make sure user metadata is saved (filename, timestamp, s3_key, etc.)

### 🟡 Additional Enhancements (Optional but Beneficial)

- [ ] Add `/results` to retrieve metadata from DynamoDB for the logged-in user
- [ ] Use presigned URLs from S3 for secure downloads
- [ ] Add `/healthz` and `/version` endpoints for testing/monitoring
- [ ] Include CPU-intensive mock task (already partially done in `/convert`)

---

## 🧠 Suggested Plan (for Teammate)

### Step 1: DynamoDB Fix
- Check AWS Console:
  - Go to DynamoDB > Tables > `AsciiMetadata`
  - Confirm it has correct schema
  - If not working, delete and recreate via Python SDK (see `dynamodb_demo.py` template)
- Ask tutor to verify your IAM role has:
  - `dynamodb:PutItem`
  - `dynamodb:GetItem`
  - `dynamodb:Query`

### Step 2: Implement `/results`
- Update `get_metadata()` route to query DynamoDB instead of in-memory list

```python
response = table.query(
    KeyConditionExpression=Key('qut-username').eq(username)
)

git clone https://github.com/YOUR_USERNAME/ascii-api.git
cd ascii-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

Then visit:
http://127.0.0.1:8000/docs

Login with admin / admin123

Copy token and authorize 🔐 in Swagger

Use /convert to upload an image

💾 AWS Resources

S3 Bucket: ascii-api-video-store

DynamoDB Table: AsciiMetadata or n11375370-ascii-db

IAM Role: AWSReservedSSO_CAB432-STUDENT_...
