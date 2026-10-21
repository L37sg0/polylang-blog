from flask import jsonify, render_template, request, abort, session, url_for, redirect
from app.repositories import post_repository, user_repository, comment_repository
from app.models.post import Post
from typing import Optional
from app.helpers import utils


def new_edit_post(post_id: Optional[int] = None):
    post = None
    if post_id:
        post = post_repository.find_by_id(post_id)
        
    return render_template('admin/new_edit_post.html', post=post)

def save_post():
    user_id = session.get('user_id')
    post = Post.from_request(request.form, user_id)
    post_repository.save(post)
    
    return redirect(url_for('admin.my_posts'))

def update_post(post_id: int):
    user_id = session.get('user_id')
    post = post_repository.find_by_id(post_id)
    
    if not post or post.user_id != user_id:
        abort(403)
        
    post.title = request.form.get('title')
    post.content = request.form.get('content')
    post.image_url = request.form.get('image_url')
    post_repository.update(post)
    
    return redirect(url_for('admin.my_posts'))

    

def delete_post(post_id: int):
    user_id = session.get('user_id')
    post = post_repository.find_by_id(post_id)
    
    if not post or post.user_id != user_id:
        abort(403)
        
    post_repository.delete(post_id)
        
    return redirect(url_for('admin.my_posts'))


def my_posts():
    user_id = session.get('user_id')
    posts = post_repository.find_by_user_id(user_id)
    
    return render_template('admin/my_posts.html', posts=posts)

def my_comments():
    user_id = session['user_id']
    comments = comment_repository.find_by_user_id_with_post_title(user_id)
    
    return render_template('admin/my_comments.html', comments=comments)
    


def new_comment():
    pass

def edit_comment():
    pass

def save_comment():
    pass

def update_comment():
    pass

def delete_comment():
    pass
