from app.models import User


def get_user_by_username(username, db):
    return db.query(User).filter(User.username == username).first()
