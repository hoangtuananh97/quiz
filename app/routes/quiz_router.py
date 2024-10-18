from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.schema.quiz import QuizCreate
from app.schema.user import UserCreate
from app.db.connection import get_db
from app.services.quiz_service import create_quiz_service
from app.websocket.manager import QuizManager

router = APIRouter()

quiz_websocket = QuizManager()


@router.websocket("/ws/{quiz_title}/{username}")
async def websocket_endpoint(websocket: WebSocket, quiz_title: str, username: str):
    print("WebSocket connection initiated for user:", username)

    try:
        # Accept the WebSocket connection
        print("Attempting to accept WebSocket connection for user:", username)
        await websocket.accept()
        print("WebSocket connection accepted for user:", username)
        # Register the client connection (in-memory or Redis-based management)
        await quiz_websocket.connect(websocket, username)

        while True:
            # Receive JSON data from the WebSocket
            data = await websocket.receive_json()
            print("Received data from user:", username, " -> Data:", data)

            event_type = data.get("event")  # e.g., "score_update", "submit_answer"

            if event_type == "score_update":
                # Update the user's score in Redis/database
                new_score = data.get("score")
                await quiz_websocket.update_score(quiz_title, username, new_score)

                # Prepare and broadcast message with updated score to all participants
                message = {
                    "event": "score_update",
                    "username": username,
                    "quiz_id": quiz_title,
                    "score": new_score
                }
                await quiz_websocket.broadcast_to_quiz(quiz_title, message)

            elif event_type == "participants_update":
                message = {
                    "event": "participants_update",
                    "username": username,
                    "quiz_id": quiz_title,
                }
                await quiz_websocket.broadcast_to_quiz(quiz_title, message)

            elif event_type == "submit_answer":
                # Process the answer submission (e.g., store in database, validate)
                answer = data.get("answer")
                print("answer", answer)
                # is_correct = await quiz_websocket.check_answer(quiz_id, answer)

                # Prepare a message with the answer result and broadcast to all participants
                message = {
                    "event": "answer_result",
                    "username": username,
                    "quiz_id": quiz_title,
                    "answer": answer,
                    "is_correct": True
                }
                await quiz_websocket.broadcast_to_quiz(quiz_title, message)

    except WebSocketDisconnect:
        # Disconnect the WebSocket and clean up resources when the client disconnects
        print(f"User {username} has disconnected.")
        await quiz_websocket.disconnect(username)

    except Exception as e:
        # Catch any other exceptions to log the error
        print(f"Error: {e}")
        await websocket.close(code=1000, reason="WebSocket closed due to an error.")


@router.post("/api/v1/quiz/{title}/join")
async def join_quiz(title: str, user_data: UserCreate, db: Session = Depends(get_db)):
    await quiz_websocket.join_quiz(title, user_data, db)
    return {"status": "joined", "title": title}


@router.post("/api/v1/quiz")
async def create_quiz(quiz_data: QuizCreate, db: Session = Depends(get_db)):
    return create_quiz_service(quiz_data, db)

