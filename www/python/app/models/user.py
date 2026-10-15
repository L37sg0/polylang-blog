from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, id, firstname, lastname, email, password,
                 created_at, updated_at, verified_at, reset_token, reset_expires_at):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at
        self.verified_at = verified_at
        self.reset_token = reset_token
        self.reset_expires_a = reset_expires_at