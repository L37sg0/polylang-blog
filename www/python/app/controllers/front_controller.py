from flask import jsonify
from app.repositories import post_repository

def index():
    posts_list = post_repository.all()
    posts = [post.to_dict() for post in posts_list]
    return jsonify(posts)

def show(post_id):
    post = post_repository.find_by_id(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
        
    return jsonify(post.to_dict())