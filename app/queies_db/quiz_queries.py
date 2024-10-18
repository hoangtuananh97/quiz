from app.models import Quiz


def get_quiz_by_title(title, db):
    return db.query(Quiz).filter(Quiz.title == title).first()
