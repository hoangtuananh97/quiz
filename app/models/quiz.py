from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, index=True, unique=True)
    users = relationship("User", back_populates="quiz")
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
