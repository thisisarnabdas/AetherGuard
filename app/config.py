from datetime import timedelta
import os
from pathlib import Path

class Config:
    # Get the base directory of your application
    BASEDIR = Path(__file__).parent.resolve()
    
    # Define the database directory and file path
    DATABASE_DIR = BASEDIR / 'database'
    DATABASE_PATH = DATABASE_DIR / 'app.db'
    
    # Ensure the database directory exists
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Flask configurations
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')  # Use environment variable or fallback
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
