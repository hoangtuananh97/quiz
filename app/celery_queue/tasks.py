from app.celery_queue.celery_app import celery_app
from app.config import settings
from app.db.connection import get_db
from app.models import Score


@celery_app.task
def process_score_update(score_entry_id: int):
    db = get_db()
    score_entry = db.query(Score).filter(Score.id == score_entry_id).first()

    score_entry.score += settings.score
    db.commit()
