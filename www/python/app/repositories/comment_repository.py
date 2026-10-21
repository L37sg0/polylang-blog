from app.helpers import db
from app.helpers import hydrate
from app.models.comment import Comment
from typing import Optional



def all() -> list[Comment]:
    query = "SELECT * FROM comments"
    rows = db.fetch_all(query)
    if not rows:
        return []

    return hydrate.comment_array(rows)

def find_by_id(comment_id: int) -> Optional[Comment]:
    query = "SELECT * FROM comments WHERE id = %s"
    row = db.fetch_one(query, (comment_id,))
    
    if not row:
        return None
        
    return hydrate.comment(row)

def find_by_id_and_user_id(comment_id: int, user_id: int) -> Optional[Comment]:
    query = "SELECT * FROM comments WHERE id = %s AND user_id=%s"
    row = db.fetch_one(query, (comment_id, user_id,))
    
    if not row:
        return None
        
    return hydrate.comment(row)

def find_by_user_id(user_id: int) -> list[Comment]:
    query = "SELECT * FROM comments where user_id = %s"
    rows = db.fetch_all(query, (user_id,))
    if not rows:
        return []
    
    return hydrate.comment_array(rows)

def find_by_user_id_with_post_title(user_id: int) -> list[dict]:
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

def find_by_post_id(post_id: int) -> list[Comment]:
    query = "SELECT * FROM comments where post_id = %s"
    rows = db.fetch_all(query, (post_id,))
    if not rows:
        return []
    return hydrate.comment_array(rows)

def find_by_post_id_with_author_name(post_id: int) -> list[dict]:
    query = """
    SELECT
        cm.id,
        cm.user_id as author_id,
        cm.content,
        CONCAT(au.firstname, ' ', au.lastname) as author_name
    FROM comments as cm
    JOIN users as au
        ON cm.user_id = au.id
    WHERE post_id = %s"""
    
    rows = db.fetch_all(query, (post_id,))
    if not rows:
        return []
    
    return rows

def save(comment: Comment) -> int:
    data = comment.to_dict()
    query = "INSERT INTO comments (user_id, post_id, content) VALUES (%s, %s, %s)"
        
    new_id = db.insert(query,(
        data['user_id'],
        data['post_id'],
        data['content'],
    ))
    
    comment.id = new_id
    
    return new_id

def update(comment: Comment) -> int:
    data = comment.to_dict()
    query = """
    UPDATE comments
    SET
        user_id=%s,
        post_id=%s,
        content=%s
    WHERE
        id=%s
    """
    updated_id = db.insert(query,(
        data['user_id'],
        data['post_id'],
        data['content'],
        data['id']
    ))
    
    return updated_id

def delete(comment_id: int) -> bool:
    query = """
    DELETE from comments where id=%s
    """
    db.insert(query, (comment_id,))
    return True
    
