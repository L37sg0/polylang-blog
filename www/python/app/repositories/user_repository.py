from app.helpers import db
from app.helpers import hydrate


def all():
    query = "SELECT * FROM users"
    rows = db.fetch_all(query)
    if not rows:
        return []
    # Хидратация: превръщаме всеки ред от речника в обект Post
    return hydrate.user_array(rows)

def find_by_id(user_id):
    query = "SELECT * FROM users WHERE id = %s"
    row = db.fetch_one(query, (user_id,))
    
    if not row:
        return None
        
    # Хидратация на единичен обект
    return hydrate.user(row)
