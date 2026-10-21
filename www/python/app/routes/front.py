from flask import Blueprint
from app.controllers import front_controller

# Създаваме Blueprint за публичната част
front_bp = Blueprint('front', __name__)

# Свързваме URL адресите директно към функциите в контролер-модула
front_bp.add_url_rule('/', 'index', front_controller.index, methods=['GET'])
front_bp.add_url_rule('/posts/<int:post_id>', 'show', front_controller.show, methods=['GET'])
front_bp.add_url_rule('/posts/by-author/<int:author_id>', 'by_author', front_controller.by_author, methods=['GET'])

front_bp.add_url_rule('/authors', 'authors', front_controller.authors, methods=['GET'])
