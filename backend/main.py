import os

import firebase_admin
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials
from routers.chat import router as chat
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware

load_dotenv(dotenv_path=".env")

app = FastAPI()

# Initialize Firebase
creds_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if creds_json is None:
    raise RuntimeError("Missing GOOGLE_APPLICATION_CREDENTIALS in environment")

credentials = credentials.Certificate("google_credentials.json")
firebase_admin.initialize_app(credentials)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

# Configure OAuth
config = Config(".env")
oauth = OAuth(config)
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url="https://oauth2.googleapis.com/token",
    access_token_params=None,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    client_kwargs={"scope": "openid email profile"},
)

app = FastAPI()


# CORS for frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat, prefix="/chat")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/")
def read_root():
    return {"message": "Chat backend is running!"}
