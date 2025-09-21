from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, ConfigDict
import uvicorn

app = FastAPI()


data = {
    "email": "test@test.com",
    "bio" : "Ndddd",
    "age": 20,
}

class UserSchema(BaseModel):
    email: EmailStr
    bio: str | None = Field(max_length=1000)

    model_config = ConfigDict(extra="forbid")

class UserAgeSchema(UserSchema):
    age: int = Field(ge=0, le=130)

users = []

@app.post("/users")
def add_user(user: UserSchema):
    users.append(user)
    return {"ok" : True, "msg" : "User added successfully!"}

@app.get("/users")
def get_users()->list[UserSchema]:
    return users



user=UserAgeSchema(**data)
print(repr(user))