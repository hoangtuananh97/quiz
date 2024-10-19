from sqlalchemy.orm import Session

from app.models.score import Score
from fastapi import HTTPException

from app.queies_db.quiz_queries import get_quiz_by_title
from app.queies_db.redis_queries import RedisQueries
from app.queies_db.user_queries import get_user_by_username
from app.schema import ScoreUpdate

import logging

logger = logging.getLogger(__name__)


def update_score_service(title: str, score_update: ScoreUpdate, db: Session):
    try:
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
    except Exception as e:
        logger.error(f"An error occurred while updating score.: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating score.")


def get_quiz_participants(title: str):
    try:
        redis_queries = RedisQueries()
        return redis_queries.get_all_quiz_data(title)
    except Exception as e:
        logger.error(f"An error occurred while getting participants.: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while getting participants.")

