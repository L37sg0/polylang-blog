from app.models.post import Post
from app.helpers import db


def all():
    query = "SELECT id, user_id, image_url, title, content, created_at, updated_at FROM posts"
    rows = db.fetch_all(query)
    
    # Хидратация: превръщаме всеки ред от речника в обект Post
    posts = []
    for row in rows:
        post = Post(
            id=row['id'],
            user_id=row['user_id'],
            image_url=row['image_url'],
            title=row['title'],
            content=row['content'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
        posts.append(post)
        
    return posts

def find_by_id(post_id):
    query = "SELECT id, user_id, image_url, title, content, created_at, updated_at FROM posts WHERE id = %s"
    row = db.fetch_one(query, (post_id,))
    
    if not row:
        return None
        
    # Хидратация на единичен обект
    return Post(
        id=row['id'],
        user_id=row['user_id'],
        image_url=row['image_url'],
        title=row['title'],
        content=row['content'],
        created_at=row['created_at'],
        updated_at=row['updated_at']
    )