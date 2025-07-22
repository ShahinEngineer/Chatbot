from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from dotenv import load_dotenv
from routers.chat import router as chat
load_dotenv(dotenv_path=".env")

# ...existing code...
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

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
