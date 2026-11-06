from flask import Blueprint, session
from app.controllers import auth_controller

auth_bp = Blueprint('auth',__name__, url_prefix='/auth')

@auth_bp.before_request
def fake_login():
    session['user_id'] = 1  # Задаваме примерен ID на потребител (напр. админа)

auth_bp.add_url_rule('/login', 'login', auth_controller.index, methods=['GET'])
auth_bp.add_url_rule('/logout', 'logout', auth_controller.logout, methods=['GET'])
auth_bp.add_url_rule('/register', 'register', auth_controller.register, methods=['GET'])

auth_bp.add_url_rule('/github-redirect', 'github_redirect', auth_controller.github_redirect, methods=['GET'])
auth_bp.add_url_rule('/forgot-password', 'forgot_password', auth_controller.forgot_password, methods=['GET'])
