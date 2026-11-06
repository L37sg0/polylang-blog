from flask import jsonify, render_template, request, abort
from app.repositories import post_repository, user_repository, comment_repository

def index():
    return render_template('auth/login.html')

def login():
    pass

def logout():
    pass

def register():
    pass

def verify_message():
    pass

def forgot_password():
    pass

def send_password_reset_link():
    pass

def reset_password():
    pass

def update_password():
    pass

def github_redirect():
    pass

def github_callback():
    pass