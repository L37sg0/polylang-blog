from app.models.base_model import BaseModel

class Comment(BaseModel):
    def __init__(self,
                 id = None,
                 user_id = None,
                 post_id = None,
                 content = None,
                 created_at = None,
                 updated_at = None
                ):
        self.id = id
        self.user_id = user_id
        self.post_id = post_id
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at
        
    @classmethod
    def from_request(cls, data: dict, user_id:int) -> 'Comment':
        return cls(
            user_id = user_id,
            content = data.get('content', '').strip(),
            post_id = data.get('post_id')
        )