from app.models.post import Post
from app.models.user import User

def post(row):
    return Post(
                id=row['id'],
                user_id=row['user_id'],
                image_url=row['image_url'],
                title=row['title'],
                content=row['content'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
    
def post_array(rows):
    array = []
    for row in rows:
        model = post(row)
        array.append(model)
        
    return array

def user(row):
    return User(
                id=row['id'],
                firstname=row['firstname'],
                lastname=row['lastname'],
                email=row['email'],
                password=row['password'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                verified_at=row['verified_at'],
                reset_token=row['reset_token'],
                reset_expires_at=row['reset_expires_at'],
            )
    
def user_array(rows):
    array = []
    for row in rows:
        model = user(row)
        array.append(model)
        
    return array 