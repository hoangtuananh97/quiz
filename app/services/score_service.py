from sqlalchemy.orm import Session

from app.models.score import Score
from fastapi import HTTPException

from app.queies_db.quiz_queries import get_quiz_by_title
from app.queies_db.redis_queries import RedisQueries
from app.queies_db.user_queries import get_user_by_username
from app.schema import ScoreUpdate


def update_score_service(title: str, score_update: ScoreUpdate, db: Session):
    quiz = get_quiz_by_title(title, db)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    user = get_user_by_username(score_update.username, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    score = Score(quiz_id=quiz.id, user_id=user.id, score=score_update.score)
    db.add(score)
    db.commit()

    return {"message:": "Successfully"}


def get_quiz_participants(title: str):
    redis_queries = RedisQueries()
    return redis_queries.get_all_quiz_data(title)
