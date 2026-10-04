from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")

        if not any(char.isalpha() for char in value):
            raise ValueError("Password must contain at least one letter")

        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")

        return value

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    role: str

    model_config = {"from_attributes": True}

""" It allows Pydantic to read data from the attributes of the SQLAlchemy User object
and convert it into the UserResponse Pydantic schema."""