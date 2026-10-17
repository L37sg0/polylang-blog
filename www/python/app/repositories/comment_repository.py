from app.helpers import db
from app.helpers import hydrate


def all():
    query = "SELECT * FROM comments"
    rows = db.fetch_all(query)
    if not rows:
        return []

    return hydrate.comment_array(rows)

def find_by_id(comment_id):
    query = "SELECT * FROM comments WHERE id = %s"
    row = db.fetch_one(query, (comment_id,))
    
    if not row:
        return None
        
    return hydrate.comment(row)

def find_by_user_id(user_id):
    query = "SELECT * FROM comments where user_id = %s"
    rows = db.fetch_all(query, (user_id,))
    if not rows:
        return []
    
    return hydrate.comment_array(rows)

def find_by_user_id_with_post_title(user_id):
    query = """
        SELECT 
            cm.id,
            cm.post_id,
            cm.content,
            cm.created_at,
            ps.title as post_title
        FROM comments as cm
        JOIN posts as ps ON
        cm.post_id=ps.id 
        WHERE cm.user_id = %s"""
        
    rows = db.fetch_all(query, (user_id,))
    if not rows:
        return []
    
    return rows

def find_by_post_id(post_id):
    query = "SELECT * FROM comments where post_id = %s"
    rows = db.fetch_all(query, (post_id,))
    if not rows:
        return []
    return hydrate.comment_array(rows)
