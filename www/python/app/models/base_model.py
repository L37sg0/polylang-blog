class BaseModel:
    def to_dict(self):
        result = {}
        
        for key, value in self.__dict__.items():
            if hasattr(value, 'isoformat'):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result
            