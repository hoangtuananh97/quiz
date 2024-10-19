from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.schema.quiz import QuizCreate
from app.schema.user import UserCreate
from app.db.connection import get_db
from app.services.quiz_service import create_quiz_service, join_quiz_service
from app.websocket.manager import QuizManager

router = APIRouter()

quiz_websocket = QuizManager()


@router.websocket("/ws/{quiz_title}/{username}")
async def websocket_endpoint(websocket: WebSocket, quiz_title: str, username: str):
    print(f"WebSocket connection initiated for user: {username} in quiz: {quiz_title}")

    try:
        # Accept the WebSocket connection
        await websocket.accept()
        print(f"WebSocket connection accepted for user: {username}")

        # Register the client connection (in-memory or Redis-based management)
        await quiz_websocket.connect(websocket, username)

        while True:
            try:
                # Receive JSON data from the WebSocket
                data = await websocket.receive_json()
                print(f"Received data from user {username} in quiz {quiz_title} -> Data: {data}")

                message = {
                    "event": "participants_update",
                    "username": username,
                    "quiz_id": quiz_title,
                    "score": 0
                }
                await quiz_websocket.broadcast_to_quiz(quiz_title, message)

            except WebSocketDisconnect:
                print(f"User {username} in quiz {quiz_title} has disconnected.")
                await quiz_websocket.disconnect(username)
                break

            except Exception as e:
                print(f"Error while processing message for user {username}: {e}")
                await websocket.close(code=1000, reason="Error occurred during WebSocket message processing.")
                break

    except Exception as e:
        print(f"Error while handling WebSocket connection for user {username}: {e}")
        await websocket.close(code=1000, reason="WebSocket closed due to an unexpected error.")


@router.post("/api/v1/quiz/{title}/join")
async def join_quiz(title: str, user_data: UserCreate, db: Session = Depends(get_db)):
    join_quiz_service(title, user_data, db)
    return {"status": "joined", "title": title}


@router.post("/api/v1/quiz")
async def create_quiz(quiz_data: QuizCreate, db: Session = Depends(get_db)):
    return create_quiz_service(quiz_data, db)
