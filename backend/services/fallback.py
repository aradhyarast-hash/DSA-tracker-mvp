# backend/services/fallback.py
def get_empty_profile(platform: str, username: str):
    return {
        "platform": platform,
        "handle": username,
        "total_solved": 0,
        "easy": 0,
        "medium": 0,
        "hard": 0,
        "rating": "--",
        "max_rating": "--",
        "rank": "--",
        "calendar_map": {},
        "topics": [],
        "badges": []
    }