from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate  
from .config import Config
from argon2 import PasswordHasher

# Initialize extensions
ph = PasswordHasher()  # Keep this one
db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize app with extensions
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    
    # Set session to be permanent
    @app.before_request
    def make_session_permanent():
        session.permanent = True
    
    # Import and register the blueprint
    from app.views import views
    app.register_blueprint(views)
    
    return app

app = create_app()