from flask import Blueprint, session
from app.controllers import admin_controller

admin_bp = Blueprint('admin',__name__, url_prefix='/admin')

@admin_bp.before_request
def fake_login():
    session['user_id'] = 1  # Задаваме примерен ID на потребител (напр. админа)

admin_bp.add_url_rule('/', 'my_posts', admin_controller.my_posts, methods=['GET'])
admin_bp.add_url_rule('/post/new', 'new_post', admin_controller.new_edit_post, methods=['GET'])
admin_bp.add_url_rule('/post/edit/<int:post_id>', 'edit_post', admin_controller.new_edit_post, methods=['GET'])
admin_bp.add_url_rule('/post/save/', 'save_post', admin_controller.save_post, methods=['POST'])
admin_bp.add_url_rule('/post/update/<int:post_id>', 'update_post', admin_controller.update_post, methods=['POST'])
admin_bp.add_url_rule('/post/delete/<int:post_id>', 'delete_post', admin_controller.delete_post, methods=['DELETE'])

admin_bp.add_url_rule('/my-comments', 'my_comments', admin_controller.my_comments, methods=['GET'])
admin_bp.add_url_rule('/comment/edit/<int:comment_id>', 'edit_comment', admin_controller.edit_comment, methods=['GET'])
admin_bp.add_url_rule('/comment/delete/<int:comment_id>', 'delete_comment', admin_controller.delete_comment, methods=['DELETE'])

