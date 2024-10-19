import redis

from app.config import settings


class RedisQueries:
    def __init__(self):
        self.redis_client = redis.from_url(settings.redis_url)

    def set_key_score(self, quiz_title):
        return f"quiz:{quiz_title}:scores"

    def update_score(self, quiz_title: str, username: str, add_score: int):
        """Updates the user's score by adding the new score to the previous score and updating the list in Redis."""
        # Save the updated score back to Redis
        self.redis_client.zincrby(self.set_key_score(quiz_title), add_score, username)

    def get_all_quiz_data(self, quiz_title: str, limit: int = 50):
        """Fetch all users and their scores for a given quiz from Redis."""

        top_users = self.redis_client.zrevrange(self.set_key_score(quiz_title), 0, limit - 1, withscores=True)
        return [
            {"username": user.decode('utf-8'), "quiz_title": quiz_title, "score": score}
            for user, score in top_users
        ]

    def add_username(self, quiz_title: str, username: str):
        redis_key = self.set_key_score(quiz_title)
        # Use ZSCORE to check if the user exists in the sorted set
        score = self.redis_client.zscore(redis_key, username)
        if score is None:
            self.redis_client.zadd(self.set_key_score(quiz_title), {username: 0})
