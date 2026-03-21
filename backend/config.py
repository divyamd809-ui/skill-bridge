import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'skillbridge-secret-key-2024')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'skillbridge.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-skillbridge-secret-2024')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000', 'null', '*']
