from flask import jsonify, render_template, request, abort, session
from app.repositories import post_repository, user_repository, comment_repository

def new_post():
    pass

def edit_post(post_id):
    pass

def save_post():
    pass

def update_post():
    pass

def delete_post(post_id):
    pass

def my_posts():
    user_id = session['user_id']
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
