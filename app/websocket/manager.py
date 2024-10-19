import redis
from fastapi import WebSocket

from app.config import settings
from app.queies_db.redis_queries import RedisQueries

import logging

logger = logging.getLogger(__name__)


class QuizManager:
    MAX_CLIENTS = settings.max_client

    def __init__(self):
        self.connected_clients = {}
        self.quizies = {}
        self.redis_client = redis.from_url(settings.redis_url)
        self.redis_queries = RedisQueries()

    async def connect(self, websocket: WebSocket, username: str, quiz_title: str):
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
        logger.info(f'User {username} connected to quiz {quiz_title}')

    async def disconnect(self, username: str, quiz_title: str):
        self.connected_clients.pop(username, None)
        self.redis_client.delete(f"client:{username}:connected")
        logger.info(
            f'User {username} disconnected from quiz {quiz_title}.'
        )

    async def broadcast_to_quiz(self, quiz_title: str, message: dict):
        """ Utility function to broadcast a message to all participants in a quiz. """
        participants = self.redis_queries.get_all_quiz_data(quiz_title)
        for participant in participants:
            if participant['username'] in self.connected_clients:
                try:
                    await self.connected_clients[participant['username']].send_json(message)
                except Exception as e:
                    logger.error(f"Error sending message to user in quiz {quiz_title}: {e}")
                logger.info(f'Broadcast message: {message} to quiz {quiz_title}')
