from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_argon2 import Argon2
from .config import Config

# Initialize extensions
db = SQLAlchemy()
argon2 = Argon2()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize app with extensions
    db.init_app(app)
    argon2.init_app(app)
    csrf.init_app(app)

    # Set session to be permanent
    @app.before_request
    def make_session_permanent():
        session.permanent = True

    # Import and register the blueprint
    from app.views import views
    app.register_blueprint(views)

    return app

app = create_app()
