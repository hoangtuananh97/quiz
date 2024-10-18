from pydantic import BaseModel
from typing import List
from .user import UserInQuiz


class QuizCreate(BaseModel):
    title: str


class QuizResponse(BaseModel):
    quiz_id: int
    title: str
    participants: List[UserInQuiz]
