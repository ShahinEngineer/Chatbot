# 🧠 Chatbot Backend (FastAPI + Firebase + OpenAI)

This is the backend service for the Chatbot project, built with **FastAPI**, integrated with **Firebase** for authentication and Firestore, and **OpenAI** for AI-powered chat responses.

---

## 🚀 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) – High-performance API framework
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup) – Authentication & Firestore
- [OpenAI API](https://platform.openai.com/docs/) – AI chat responses
- [flake8](https://flake8.pycqa.org/en/latest/) – Code linting
- [python-dotenv](https://pypi.org/project/python-dotenv/) – Load environment variables

---

## 📦 Setup Instructions
### python v 3.11

### 1.Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```
#### 2.📁 Navigate to the backend directory
``` bash
cd backend
```
#### 3. 📁 copy your google credintals in /backend folder
    - google_credentials.json

#### 4. 📁 create local env
    - copy local.env file in .env
    - add your securts keys there

### 5. 🏁 Run Backend Side

```bash
pip3 install -r requirements.txt

uvicorn main:app --reload
```

### API Documentation
    - http://localhost:8000/docs#/