# AI-Powered Workflow Automation Assistant

> FYP Project — University of Lahore (CSDL Program)

## Project Overview

An AI-powered backend system that connects to Gmail,
automatically classifies emails using Machine Learning,
and extracts tasks and deadlines — helping users manage
their workflow intelligently.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + FastAPI |
| Database | MySQL + SQLAlchemy |
| Authentication | JWT Tokens + bcrypt |
| Email Integration | Gmail API + OAuth 2.0 |
| AI/ML | scikit-learn (Naive Bayes + TF-IDF) |
| NLP | NLTK |
| API Docs | Swagger UI (auto-generated) |


## Features Completed (30% Milestone)

-  User Registration & Login with JWT
-  Gmail OAuth 2.0 Integration
-  Email Fetching & Storage in MySQL
-  ML Email Classification (Naive Bayes + TF-IDF)
-  Task Extraction from Emails
-  Dashboard API
-  RESTful API with Swagger Documentation

## Project Structure
backend/
├── app.py              ← Main entry point
├── config.py           ← Environment settings
├── database/
│   └── db.py           ← Database connection
├── models/
│   ├── user_model.py   ← User table
│   ├── email_model.py  ← Email table
│   └── task_model.py   ← Task table
├── routes/
│   ├── auth_routes.py      ← Login/Register APIs
│   ├── gmail_routes.py     ← Gmail OAuth APIs
│   ├── classify_routes.py  ← ML Classification APIs
│   ├── task_routes.py      ← Task Extraction APIs
│   └── dashboard_routes.py ← Dashboard API
├── services/
│   ├── gmail_service.py        ← Gmail API logic
│   ├── classifier_service.py   ← ML Model
│   ├── task_extractor.py       ← Task extraction
│   └── training_data.py        ← ML training data
└── requirements.txt

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | /auth/register | Register new user |
| POST | /auth/login | Login + get JWT token |

### Gmail
| Method | Endpoint | Description |
|---|---|---|
| GET | /auth/gmail/connect | Get Google OAuth URL |
| GET | /auth/gmail/callback | OAuth callback |
| GET | /auth/gmail/emails | Fetch & store emails |
| GET | /auth/gmail/emails/db | Get stored emails |

### Classification
| Method | Endpoint | Description |
|---|---|---|
| GET | /emails/classify/model-info | ML model details |
| POST | /emails/classify/single | Classify one email |
| POST | /emails/classify/all | Classify all emails |
| GET | /emails/classify/summary | Category breakdown |

### Tasks
| Method | Endpoint | Description |
|---|---|---|
| POST | /emails/tasks/extract | Extract tasks |
| GET | /emails/tasks/all | Get all tasks |
| GET | /emails/tasks/summary | Priority breakdown |

### Dashboard
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/dashboard/summary | Full system overview |
| GET | /api/dashboard/health | Health check |



## How to Run

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd backend

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup .env file
DB_HOST=localhost
DB_PORT=3306
DB_NAME=workflow_db
DB_USER=root
DB_PASSWORD=yourpassword

# 5. Run the server
uvicorn app:app --reload
```

Open Swagger docs at: **http://127.0.0.1:8000/docs**



## ML Model Details

- **Algorithm:** Naive Bayes Classifier
- **Vectorization:** TF-IDF (unigrams + bigrams)
- **Categories:** urgent, spam, newsletter, social, important, general
- **Accuracy:** 100% on test set
- **Training Samples:** 60 labeled emails



## Developer

**Name:** Raghfa Shahid,Ayesha Amanat
**University:** University of Lahore
**Program:** CSDL