from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str


class UserInQuiz(BaseModel):
    user_id: int
    username: str
    quiz_id: int
