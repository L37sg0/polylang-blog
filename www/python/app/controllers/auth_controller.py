from flask import jsonify, render_template, request, abort, redirect, url_for, session
from app.repositories import post_repository, user_repository, comment_repository

def login():
    if session.get('user_id'):
        return redirect(url_for('admin.my_posts'))
    
    if request.method == 'GET':
        return render_template('auth/login.html')

    user = user_repository.find_by_email(request.form.get('email'))
    if not user:
        return redirect(url_for('auth.login'))
    
    password_correct = user.password == request.form.get('password')
    if not password_correct:
        return redirect(url_for('auth.login'))
    
    session['user_id'] = user.id
    return redirect(url_for('admin.my_posts'))


def logout():
    session['user_id'] = None
    return redirect(url_for('front.index'))

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