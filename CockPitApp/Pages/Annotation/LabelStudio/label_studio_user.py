from pydantic import BaseModel
from typing import Optional

class LabelStudioUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    phone: str = ''
    active_organization: Optional[int] = None
    allow_newsletters: Optional[bool] = None