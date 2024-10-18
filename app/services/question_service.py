from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.models import Quiz, Score, User
from app.models.question import Question, Answer
from app.queies_db.redis_queries import RedisQueries
from app.schema.question import AnswerSubmitBase

router = APIRouter()


def get_current_question_service(quiz_title: str, db: Session):
    # Fetch the quiz based on the title
    quiz = db.query(Quiz).filter(Quiz.title == quiz_title).first()
    answers = []
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # Get the current question of the quiz
    current_question = db.query(Question).filter(Question.quiz_id == quiz.id, Question.is_active == True).first()

    if current_question:
        # Get the possible answers for the current question
        answers = db.query(Answer).filter(Answer.question_id == current_question.id).all()

    # Prepare the response
    return {
        "question_id": current_question.id if current_question else None,
        "question_text": current_question.text if current_question else None,
        "answers": [
            {"id": answer.id, "answer_text": answer.text} for answer in answers
        ]
    }


def submit_answer_service(quiz_title: str, answer_submit: AnswerSubmitBase, db: Session):
    # Fetch the quiz
    quiz = db.query(Quiz).filter(Quiz.title == quiz_title).first()

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # Fetch the question
    question = db.query(Question).filter(Question.id == answer_submit.question_id, Question.quiz_id == quiz.id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Fetch the selected answer
    selected_answer = db.query(Answer).filter(Answer.id == answer_submit.answer_id, Answer.question_id == question.id).first()

    if not selected_answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    # Fetch the user
    user = db.query(User).filter(User.username == answer_submit.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch the user's score for this quiz
    score_entry = db.query(Score).filter(Score.quiz_id == quiz.id, Score.user_id == user.id).first()

    add_score = 10
    # Check if the answer is correct
    if selected_answer.is_correct:
        score_entry.score += add_score
        db.commit()

        redis_queries = RedisQueries()
        redis_queries.update_score(quiz_title, answer_submit.username, add_score)

    return {
        "correct": selected_answer.is_correct,
        "updated_score": score_entry.score
    }
