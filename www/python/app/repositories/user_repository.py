from app.helpers import db
from app.helpers import hydrate
from app.models.user import User
from typing import Optional

def all() -> list[User]:
    query = "SELECT * FROM users"
    rows = db.fetch_all(query)
    if not rows:
        return []
    # Хидратация: превръщаме всеки ред от речника в обект Post
    return hydrate.user_array(rows)

def all_with_stats() -> list[dict]:
    query = """
        SELECT 
            us.id,
            us.firstname,
            us.lastname,
            ( SELECT COUNT(*) from posts as ps WHERE ps.user_id = us.id ) as posts_stat,
            ( SELECT COUNT(*) from comments as cm WHERE cm.user_id = us.id ) as comments_stat             
        FROM users as us           
    """
    
    rows = db.fetch_all(query)
    if not rows:
        return []
    
    return rows

def find_by_id(user_id: int) -> Optional[User]:
    query = "SELECT * FROM users WHERE id = %s"
    row = db.fetch_one(query, (user_id,))
    
    if not row:
        return None
        
    # Хидратация на единичен обект
    return hydrate.user(row)
