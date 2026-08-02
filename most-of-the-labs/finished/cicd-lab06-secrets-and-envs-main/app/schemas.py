"""Pydantic schemas, mirrors src/modules/users/user.schema.ts (zod)."""
from pydantic import BaseModel, EmailStr, Field, model_validator


class CreateUser(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr


class UpdateUser(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None

    @model_validator(mode="after")
    def at_least_one(self) -> "UpdateUser":
        if self.name is None and self.email is None:
            raise ValueError("At least one field required")
        return self


class UserOut(BaseModel):
    id: str
    name: str
    email: str
    createdAt: str
