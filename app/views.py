from flask import Blueprint, render_template, url_for, redirect, flash, session, request
from functools import wraps
from app import db
from app.forms import RegistrationForm, LoginForm, PasswordForm, GeneratePasswordForm
from app.models import User, StoredPassword
import random
import string

# Create a Blueprint
views = Blueprint('views', __name__)

# Helper function for generating random passwords
def generate_random_password(length):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(characters) for i in range(length))

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for("views.login"))
        return f(*args, **kwargs)
    return decorated_function

@views.route("/")
def home():
    if 'user_id' in session:
        return redirect(url_for("views.dashboard"))
    else:
        return redirect(url_for("views.login"))

@views.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully!", "success")
        return redirect(url_for("views.login"))
    return render_template("register.html", form=form)

@views.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session.clear()  # Clear any existing session data
            session['user_id'] = user.id  # Set the new session
            return redirect(url_for("views.dashboard"))
        else:
            flash("Login unsuccessful. Please check your credentials.", "danger")
    return render_template("login.html", form=form)

@views.route("/logout")
def logout():
    session.clear()  # Clears the session data
    flash("You have been logged out.", "success")
    return redirect(url_for("views.login"))

@views.route("/dashboard")
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    stored_passwords = StoredPassword.query.filter_by(user_id=user.id).all()
    return render_template("dashboard.html", stored_passwords=stored_passwords)

@views.route("/add_password", methods=['GET', 'POST'])
@login_required
def add_password():
    form = PasswordForm()
    generated_password = None

    if 'generate_password' in request.form:
        # Generate a random password if "Generate Password" button is clicked
        length = 16  # Default length for generated password
        generated_password = generate_random_password(length)
        form.password.data = generated_password

    if form.validate_on_submit() and 'submit' in request.form:
        # Save the password entry when "Add Password" button is clicked
        password_entry = StoredPassword(
            title=form.title.data,
            username=form.username.data,
            user_id=session['user_id']
        )
        password_entry.set_password(form.password.data)
        db.session.add(password_entry)
        db.session.commit()
        flash("Password stored successfully!", "success")
        return redirect(url_for("views.dashboard"))

    return render_template("add_password.html", form=form, generated_password=generated_password)
