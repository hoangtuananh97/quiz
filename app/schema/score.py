from pydantic import BaseModel


class ScoreUpdate(BaseModel):
    username: str
    score: int


class Participant(BaseModel):
    username: str
    title: str
    score: int
