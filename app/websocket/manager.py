from typing import List

import redis
from fastapi import WebSocket, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
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
            join_quiz_service(title, user_data, db)

        redis_key = f"quiz:{quiz.title}:user:{user_data.username}:score"
        user_exists = self.redis_client.exists(redis_key)

        if not user_exists:
            self.redis_client.set(f"quiz:{quiz.title}:user:{user_data.username}:score", 0)

        # Prepare a notification message to send to other participants
        message_data = {
            "sender": "system",
            "quiz_title": quiz.title,
            "score": 0,
            "username": user_data.username,
            "event": "participants_update"
        }

        # Retrieve all participants for the quiz from Redis
        participants = self.redis_queries.get_all_quiz_data(quiz.title)

        # Notify all participants except the new joiner
        for participant in participants:
            if participant['username'] != user_data.username and participant['username'] in self.connected_clients:
                await self.connected_clients[participant['username']].send_json(message_data)

    async def broadcast_to_quiz(self, quiz_title: str, message: dict):
        """ Utility function to broadcast a message to all participants in a quiz. """
        participants = await self.redis_queries.get_all_quiz_data(quiz_title)
        for participant in participants:
            print(participant['username'], self.connected_clients)
            if participant['username'] in self.connected_clients:
                await self.connected_clients[participant['username']].send_json(message)

# class MessageManager:
#     MAX_MESSAGES = 500
#
#     def __init__(self, quiz_manager: QuizManager):
#         self.quiz_manager = quiz_manager
#         self.redis_client = redis.from_url(settings.redis_url)
#
#     async def handle_message(self, message: dict, client_id, websocket: WebSocket):
#         # Mark that the client has sent a message
#         await self.redis_client.set(f"client:{message.sender}:message_sent", "1")
#
#         # Check if the message limit has been reached
#         if not self.semaphore.locked():
#             async with self.semaphore:
#                 if not message.room_id:
#                     raise HTTPException(status_code=400, detail="Room ID is required for messaging.")
#
#                 if self.is_message_acceptable(message):
#                     message.status = "success"
#                     reply_content = f"Your message in room {message.room_id} saying '{message.content}' has been received and accepted."
#                 else:
#                     message.status = "rejected"
#                     reply_content = f"Your message in room {message.room_id} was not accepted because it was sent outside of acceptable hours."
#
#                 message.reply = reply_content
#                 message_data = message.dict()
#
#                 # Save the message to the database using Celery
#                 save_message_to_db.delay(message_data)
#
#                 # If the message was accepted, send it to the room
#                 if message.status == "success":
#                     await self.room_manager.send_message_to_room(message.sender, client_id, message)
#
#                 # Send the reply back to the sender if still connected
#                 if message.sender in self.room_manager.connected_clients:
#                     reply_data = {
#                         "sender": "Server",
#                         "room_id": message.room_id,
#                         "original_message": message.content,
#                         "reply": reply_content,
#                         "status": message.status,
#                         "timestamp": datetime.utcnow().isoformat()
#                     }
#                     await websocket.send_json(reply_data)
#                 else:
#                     # Mark the reply as unsuccessful if the client has disconnected
#                     message.status = "unsuccessful"
#                     message.reply = f"Message delivery failed: client {message.sender} disconnected before receiving the reply."
#                     save_message_to_db.delay(message.dict())
#         else:
#             # If the message limit is reached, notify the sender
#             await websocket.send_json({
#                 "sender": "Server",
#                 "room_id": message.room_id,
#                 "status": "rejected",
#                 "reply": "The server is currently busy. Please try again later.",
#                 "timestamp": datetime.utcnow().isoformat()
#             })
