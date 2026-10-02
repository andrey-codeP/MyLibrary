from pydantic import BaseModel, Field, ConfigDict


class UserInDb(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(
        ...,
        min_length=6,
        max_length=20,
        description="простой пароль от 6 символов до 20",
    )

    model_config = ConfigDict(from_attributes=True)
