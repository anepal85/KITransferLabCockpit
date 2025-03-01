from pydantic import BaseModel, EmailStr


class User(BaseModel):
    '''
        This class is designed to implement user Model for YOLO but have not been used
    '''
    name: str
    role: str
    email: EmailStr
    password: str

    def login(self, password):
        return self.password == password

    @staticmethod
    def authenticate(username, password):
        # replace this with your authentication logic
        if username == 'admin' and password == 'admin123':
            return User(
                name='Admin User',
                role='admin',
                email='admin@example.com',
                password='admin123'
            )
        return None
