from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Score
from app.models.quiz import Quiz
from app.models.user import User
from app.queies_db.quiz_queries import get_quiz_by_title
from app.queies_db.redis_queries import RedisQueries
from app.queies_db.user_queries import get_user_by_username
from app.schema.user import UserCreate
from app.schema.quiz import QuizCreate


def join_quiz_service(title: str, user_data: UserCreate, db: Session):
    quiz = get_quiz_by_title(title, db)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    user = get_user_by_username(user_data.username, db)
    if not user:
        user = User(username=user_data.username, quiz_id=quiz.id)
        db.add(user)
        db.commit()

    # Fetch or create the user's score for this quiz
    score_entry = db.query(Score).filter(Score.quiz_id == quiz.id, Score.user_id == user.id).first()

    if not score_entry:
        score_entry = Score(user_id=user.id, quiz_id=quiz.id, score=0)
        db.add(score_entry)
        db.commit()

    redis_queries = RedisQueries()
    redis_queries.add_username(quiz.title, user_data.username)

    return user


def create_quiz_service(quiz_data: QuizCreate, db: Session):
    quiz = Quiz(title=quiz_data.title)
    db.add(quiz)
    db.commit()
    return {"title": quiz.title}
