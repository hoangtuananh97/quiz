import redis

from app.config import settings


class RedisQueries:
    def __init__(self):
        self.redis_client = redis.from_url(settings.redis_url)

    def update_score(self, quiz_title: str, username: str, new_score: int):
        """Updates the user's score by adding the new score to the previous score and updating the list in Redis."""

        # Get the previous score from Redis, if it doesn't exist, start with 0
        previous_score = self.redis_client.get(f"quiz:{quiz_title}:user:{username}:score")
        previous_score = int(previous_score) if previous_score else 0

        # Add the new score to the previous score
        updated_score = previous_score + new_score

        # Save the updated score back to Redis
        self.redis_client.set(f"quiz:{quiz_title}:user:{username}:score", updated_score)

    def find_keys_matching_pattern(self, pattern: str):
        cursor = 0
        matching_keys = []

        while True:
            # Scan through the keys using a pattern
            cursor, keys = self.redis_client.scan(cursor, match=pattern)

            # Append all matching keys
            matching_keys.extend(keys)

            # If cursor is 0, we are done scanning
            if cursor == 0:
                break

        return matching_keys

    def get_all_quiz_data(self, quiz_title: str):
        """Fetch all users and their scores for a given quiz from Redis."""

        # Use SCAN to find all user score keys for the quiz
        keys = self.find_keys_matching_pattern(f"quiz:{quiz_title}:user:*:score")
        if not keys:
            return []

        # Fetch all the scores from Redis
        scores = self.redis_client.mget(*keys)
        result = []

        for key, score in zip(keys, scores):
            # Extract username from the key (e.g., "quiz:GeneralKnowledge:user:alice:score")
            key_parts = key.decode('utf-8').split(":")
            username = key_parts[3]

            # Prepare the final result with username, score, and quiz_title
            result.append({
                "username": username,
                "score": int(score),
                "quiz_title": quiz_title
            })

        return result
