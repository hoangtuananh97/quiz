from pydantic import BaseModel
from typing import List, Optional


# Answer schema
class AnswerBase(BaseModel):
    text: str
    is_correct: Optional[bool] = False


class AnswerCreate(AnswerBase):
    pass


class AnswerOut(AnswerBase):
    id: int

    class Config:
        orm_mode = True


class AnswerSubmitBase(BaseModel):
    username: str
    question_id: int
    answer_id: int


# Question schema
class QuestionBase(BaseModel):
    text: str
    is_active: Optional[bool] = True


class QuestionCreate(QuestionBase):
    answers: List[AnswerCreate]


class QuestionOut(QuestionBase):
    id: int
    answers: List[AnswerOut]

    class Config:
        orm_mode = True
