import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Fliph106@localhost:5433/login/api'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')