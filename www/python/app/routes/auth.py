from flask import Blueprint, session
from app.controllers import admin_controller

auth_bp = Blueprint('auth',__name__, url_prefix='/admin')

@auth_bp.before_request
def fake_login():
    session['user_id'] = 1  # Задаваме примерен ID на потребител (напр. админа)

auth_bp.add_url_rule('/login', 'login', admin_controller.my_posts, methods=['GET'])
auth_bp.add_url_rule('/logout', 'logout', admin_controller.my_comments, methods=['GET'])
