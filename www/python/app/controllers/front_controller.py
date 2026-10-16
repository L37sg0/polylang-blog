from flask import jsonify, render_template, request, abort
from app.repositories import post_repository, user_repository

def index():
    posts = post_repository.all()
    return render_template('front/index.html', posts=posts, title="Latest Posts")

def show(post_id):
    post = post_repository.find_by_id(post_id)
    if not post:
        abort(404)
    
    author = user_repository.find_by_id(post.user_id)
    author_name = author.get_full_name()
        
    return render_template('front/show.html', post=post, author_name=author_name)

def by_author(author_id):
    author = user_repository.find_by_id(author_id)
    if not author:
        abort(404)
    
    posts = post_repository.find_by_user_id(author_id)
    author_name = author.get_full_name()
    if not posts:
        abort(404)
    
    return render_template('front/index.html', posts=posts, title=f"Posts by author {author_name}")
    