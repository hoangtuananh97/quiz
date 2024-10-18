from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.quiz import Quiz
from app.models.user import User
from app.queies_db.quiz_queries import get_quiz_by_title
from app.schema.user import UserCreate
from app.schema.quiz import QuizCreate


def join_quiz_service(title: str, user_data: UserCreate, db: Session):
    quiz = get_quiz_by_title(title, db)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    user = User(username=user_data.username, quiz_id=quiz.id)
    db.add(user)
    db.commit()
    return {"message": f"User {user.username} joined quiz {quiz.title}"}


def create_quiz_service(quiz_data: QuizCreate, db: Session):
    quiz = Quiz(title=quiz_data.title)
    db.add(quiz)
    db.commit()
    return {"title": quiz.title}
