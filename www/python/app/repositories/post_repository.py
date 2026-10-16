from app.helpers import db
from app.helpers import hydrate


def all():
    query = "SELECT * FROM posts"
    rows = db.fetch_all(query)
    if not rows:
        return []
    # Хидратация: превръщаме всеки ред от речника в обект Post
    return hydrate.post_array(rows)

def find_by_id(post_id):
    query = "SELECT * FROM posts WHERE id = %s"
    row = db.fetch_one(query, (post_id,))
    
    if not row:
        return None
        
    # Хидратация на единичен обект
    return hydrate.post(row)

def find_by_user_id(user_id):
    query = "SELECT * FROM posts where user_id = %s"
    rows = db.fetch_all(query, (user_id,))
    if not rows:
        return []
    
    return hydrate.post_array(rows)