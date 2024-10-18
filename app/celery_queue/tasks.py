from app.queue.celery_app import celery_app


@celery_app.task
def process_score_update(user_id: int, quiz_id: int, score: int):
    # Logic to update score in the database
    print(f"Processing score update for user {user_id} in quiz {quiz_id} with score {score}")
    # Add actual database logic here
