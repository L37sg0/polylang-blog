from app.models.base_model import BaseModel

class Post(BaseModel):
    def __init__(self, 
                 id=None,
                 user_id=None,
                 image_url=None,
                 title=None, 
                 content=None,
                 created_at=None,
                 updated_at=None
                ):
        self.id = id
        self.user_id = user_id
        self.image_url = image_url
        self.title = title
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at
        
    def from_request(request) -> Post:
        self.user_id = request.form.get('user_id')
        self.image_url = request.form.get('image_url')
        self.title = request.form.get('title')
        self.content = request.form.get('content')
        
        return self
        
        