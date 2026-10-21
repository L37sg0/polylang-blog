from typing import Optional
from app.models.post import Post
from app.helpers import db
from app.helpers import hydrate


def all() -> list[Post]:
    query = "SELECT * FROM posts"
    rows = db.fetch_all(query)
    if not rows:
        return []
    # Хидратация: превръщаме всеки ред от речника в обект Post
    return hydrate.post_array(rows)

def find_by_id(post_id: int) -> Optional[Post]:
    query = "SELECT * FROM posts WHERE id = %s"
    row = db.fetch_one(query, (post_id,))
    
    if not row:
        return None
        
    # Хидратация на единичен обект
    return hydrate.post(row)

def find_by_user_id(user_id: int) -> list[Post]:
    query = "SELECT * FROM posts where user_id = %s"
    rows = db.fetch_all(query, (user_id,))
    if not rows:
        return []
    
    return hydrate.post_array(rows)

def save(post: Post) -> int:
    data = post.to_dict()
    query = "INSERT INTO posts (user_id, image_url, title, content) VALUES (%s, %s, %s, %s)"
        
    new_id = db.insert(query,(
        data['user_id'],
        data['image_url'],
        data['title'],
        data['content'],
    ))
    
    post.id = new_id
    
    return new_id

def update(post: Post) -> int:
    data = post.to_dict()
    query = """
    UPDATE posts
    SET
        user_id=%s,
        image_url=%s,
        title=%s,
        content=%s
    WHERE
        id=%s
    """
    updated_id = db.insert(query,(
        data['user_id'],
        data['image_url'],
        data['title'],
        data['content'],
        data['id']
    ))
    
    return updated_id

def delete(post_id: int) -> bool:
    query = """
    DELETE from posts where id=%s
    """
    db.insert(query, (post_id,))
    return True
    