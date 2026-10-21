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
        
    @classmethod
    def from_request(cls, data: dict, user_id: int) -> 'Post':
        return cls(
            user_id=user_id,
            title=data.get('title', '').strip(),
            content=data.get('content', '').strip(),
            image_url=data.get('image_url')
        )
        
        