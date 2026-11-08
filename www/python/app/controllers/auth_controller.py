from flask import render_template, request, redirect, url_for, session
from app.repositories import user_repository
from app.models.user import User
from app.helpers.utils import check_password

def login():
    if session.get('user_id'):
        return redirect(url_for('admin.my_posts'))
    
    if request.method == 'GET':
        return render_template('auth/login.html')

    user = user_repository.find_by_email(request.form.get('email'))
    if not user:
        return redirect(url_for('auth.login'))
    
    password_correct = check_password(request.form.get('password'), user.password)
    if not password_correct:
        return redirect(url_for('auth.login'))
    
    session['user_id'] = user.id
    return redirect(url_for('admin.my_posts'))


def logout():
    session.clear()
    return redirect(url_for('front.index'))

def register():
    if session.get('user_id'):
        return redirect(url_for('admin.my_posts'))
    
    if request.method == 'GET':
        return render_template('auth/register.html')

    user = User.from_request(request.form)
    if not user:
        return render_template('auth/register.html')
    
    user_id = user_repository.save(user)
    session['user_id'] = user_id
    return redirect(url_for('admin.my_posts'))

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