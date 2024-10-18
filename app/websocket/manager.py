from typing import List

import redis
from fastapi import WebSocket, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Score
from app.queies_db.quiz_queries import get_quiz_by_title
from app.queies_db.redis_queries import RedisQueries
from app.queies_db.user_queries import get_user_by_username
from app.schema import UserCreate
from app.services.quiz_service import join_quiz_service


class QuizManager:
    MAX_CLIENTS = 50

    def __init__(self):
        self.connected_clients = {}
        self.quizies = {}
        self.redis_client = redis.from_url(settings.redis_url)
        self.redis_queries = RedisQueries()

    async def connect(self, websocket: WebSocket, username: str):
        # Check if the client is already connected by looking up Redis
        if self.redis_client.exists(f"client:{username}:connected"):
            await websocket.close(code=1008, reason="Client already has an active connection.")
            return

        # Check if the maximum number of clients is reached
        if len(self.connected_clients) >= self.MAX_CLIENTS:
            await websocket.close(code=1008, reason="Maximum client limit reached. Try again later.")
            return

        # await websocket.accept()
        self.connected_clients[username] = websocket
        # Set the client as connected in Redis
        self.redis_client.set(f"client:{username}:connected", "1")
        # Set expiration time for 1 hour (optional)
        # await self.redis_client.expire(f"client:{username}:connected", 3600)

    async def disconnect(self, username: str):
        self.connected_clients.pop(username, None)
        self.redis_client.delete(f"client:{username}:connected")

    async def update_score(self, quiz_title: str, username: str, new_score: int):
        # Update the user's score in Redis
        await self.redis_queries.update_score(quiz_title, username, new_score)

    async def join_quiz(self, title: str, user_data: UserCreate, db: Session):
        quiz = get_quiz_by_title(title, db)
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        user = get_user_by_username(user_data.username, db)
        if not user:
            user = join_quiz_service(title, user_data, db)

        # Fetch or create the user's score for this quiz
        score_entry = db.query(Score).filter(Score.quiz_id == quiz.id, Score.user_id == user.id).first()

        if not score_entry:
            score_entry = Score(user_id=user.id, quiz_id=quiz.id, score=0)
            db.add(score_entry)
            db.commit()

        redis_key = f"quiz:{quiz.title}:user:{user_data.username}:score"
        user_exists = self.redis_client.exists(redis_key)

        if not user_exists:
            self.redis_client.set(f"quiz:{quiz.title}:user:{user_data.username}:score", 0)

    async def broadcast_to_quiz(self, quiz_title: str, message: dict):
        """ Utility function to broadcast a message to all participants in a quiz. """
        participants = self.redis_queries.get_all_quiz_data(quiz_title)
        print("participants", participants)
        for participant in participants:
            print(participant['username'], self.connected_clients)
            if participant['username'] in self.connected_clients:
                await self.connected_clients[participant['username']].send_json(message)
