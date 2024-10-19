from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.routes.quiz_router import quiz_websocket
from app.schema.question import AnswerSubmitBase
from app.services.question_service import get_current_question_service, submit_answer_service

router = APIRouter()


@router.get("/api/v1/quiz/{quiz_title}/current_question")
async def get_current_question(quiz_title: str, db: Session = Depends(get_db)):
    return get_current_question_service(quiz_title, db)


@router.post("/api/v1/quiz/{quiz_title}/submit_answer")
async def submit_answer(
        quiz_title: str, answer_submit: AnswerSubmitBase, db: Session = Depends(get_db)
):
    result = submit_answer_service(quiz_title, answer_submit, db)
    message = {
        "event": "score_update",
        "quiz_title": quiz_title,
        "username": answer_submit.username,
        "score": result['updated_score']
    }
    await quiz_websocket.broadcast_to_quiz(quiz_title, message)
    return result
