
Assignment 1 - REST API Project - Response to Criteria
================================================

Overview
------------------------------------------------

- **Name:** Davie Tran
- **Student number:** n11375370
- **Application name:** ASCII Art API
- **Two line description:** This API takes image uploads, converts them to ASCII art using a CPU-intensive algorithm, and returns the result. JWT-based authentication is used.

Core criteria
------------------------------------------------

### Containerise the app

- **ECR Repository name**: ascii-api
- **Video timestamp:** 0:10
- **Relevant files:**
    - /Dockerfile

### Deploy the container

- **EC2 instance ID**: i-0240b3a438cba470e
- **Video timestamp:** 0:30

### User login

- **One line description:** Hardcoded user auth with JWT token
- **Video timestamp:** 0:40
- **Relevant files:**
    - main.py

### REST API

- **One line description:** REST API with /login and /convert endpoints
- **Video timestamp:** 0:50
- **Relevant files:**
    - main.py

### Two kinds of data

#### First kind

- **One line description:** Uploaded images
- **Type:** Unstructured
- **Rationale:** Processed directly from upload
- **Video timestamp:** 1:15
- **Relevant files:**
    - /data/
    - main.py

#### Second kind

- **One line description:** User credentials
- **Type:** Structured
- **Rationale:** Used for auth
- **Video timestamp:** 1:20
- **Relevant files:**
    - main.py

### CPU intensive task

- **One line description**: Image converted to ASCII using numpy and Pillow
- **Video timestamp:** 2:00
- **Relevant files:**
    - ascii_art/ascii_converter.py

### CPU load testing

- **One line description**: Repeated curl requests to trigger multiple conversions
- **Video timestamp:** 2:30
- **Relevant files:**
    - load_test.sh or curl loop
    - AWS Monitoring

Additional criteria
------------------------------------------------

### Extensive REST API features

- **One line description**: Proper status codes, error messages, and token validation
- **Video timestamp:** 1:00
- **Relevant files:**
    - main.py

### External API(s)

- **One line description**: Not implemented
- **Video timestamp:** N/A
- **Relevant files:**
    - N/A

### Additional kinds of data

- **One line description**: Not attempted
- **Video timestamp:** N/A

### Custom processing

- **One line description**: Image-to-ASCII as core custom logic
- **Video timestamp:** 1:45
- **Relevant files:**
    - ascii_art/

### Infrastructure as code

- **One line description**: Not implemented
- **Video timestamp:** N/A
