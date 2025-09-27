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

## ✅ How to Run

```bash
git clone https://github.com/yourusername/ascii-api.git
cd ascii-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
