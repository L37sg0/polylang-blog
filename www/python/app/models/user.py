from app.models.base_model import BaseModel
from app.helpers.utils import hash_password

class User(BaseModel):
    def __init__(self,
                 id = None,
                 firstname = None,
                 lastname = None,
                 email = None,
                 password = None,
                 created_at = None,
                 updated_at = None,
                 verified_at = None,
                 reset_token = None,
                 reset_expires_at = None
                 ):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at
        self.verified_at = verified_at
        self.reset_token = reset_token
        self.reset_expires_at = reset_expires_at
        
    def get_full_name(self):
        return f"{self.firstname} {self.lastname}"
    
    @classmethod
    def from_request(cls, data: dict) -> 'User':
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        
        if not password or password != password_confirm:
            return None
        
        password_hashed = hash_password(password)
        
        return cls(
            firstname = data.get('firstname'),
            lastname = data.get('lastname'),
            email = data.get('email'),
            password = password_hashed
        )