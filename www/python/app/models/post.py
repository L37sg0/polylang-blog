from app.models.base_model import BaseModel

class Post(BaseModel):
    def __init__(self, id, user_id, image_url, title, content, created_at, updated_at):
        self.id = id
        self.user_id = user_id
        self.image_url = image_url
        self.title = title
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at