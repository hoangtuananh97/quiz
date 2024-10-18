from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.connection import get_db
from app.schema import ScoreUpdate
from app.services.score_service import update_score_service, get_quiz_participants

router = APIRouter()


@router.put("/api/v1/quiz/{title}/scores")
async def update_score(title: str, score_update: ScoreUpdate, db: Session = Depends(get_db)):
    return update_score_service(title, score_update, db)


@router.get("/api/v1/quiz/{quiz_title}/scores")
async def get_scores(quiz_title: str, _: Session = Depends(get_db)):
    return get_quiz_participants(quiz_title)
