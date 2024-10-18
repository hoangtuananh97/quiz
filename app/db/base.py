# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.quiz import Quiz  # noqa
from app.models.score import Score  # noqa
from app.models.question import Question  # noqa
from app.models.question import Answer  # noqa
