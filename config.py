import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
    MONGO_URI = os.getenv("MONGO_URI")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    