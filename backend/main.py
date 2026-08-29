import os
import json
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

from services import get_platform_data

load_dotenv()

app = FastAPI(title="DSA Tracker API")

# Allow frontend Live Server & local calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    try:
        return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    except Exception as e:
        print("Database connection notice:", e)
        return None


# -------------------------------------------------------------
# 1. HEALTH CHECK
# -------------------------------------------------------------
@app.get("/")
def home():
    return {"message": "DSA Tracker Modular API Running Successfully!"}


# -------------------------------------------------------------
# 2. MODULAR MULTI-PLATFORM TELEMETRY ROUTE
# -------------------------------------------------------------
@app.get("/api/fetch-stats")
def fetch_stats(platform: str, username: str):
    # Fetch from dedicated services module
    data = get_platform_data(platform, username)
    
    if not data:
        raise HTTPException(
            status_code=404, 
            detail=f"User '{username}' not found on {platform.upper()} or platform is unreachable."
        )

    # Persist Snapshot to Supabase (Fail-Safe)
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            query = """
                INSERT INTO platform_stats 
                (platform, handle, total_solved, easy_solved, medium_solved, hard_solved, ranking, rating, max_rating, badges, topic_stats, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (platform, handle) 
                DO UPDATE SET 
                    total_solved = EXCLUDED.total_solved,
                    easy_solved = EXCLUDED.easy_solved,
                    medium_solved = EXCLUDED.medium_solved,
                    hard_solved = EXCLUDED.hard_solved,
                    ranking = EXCLUDED.ranking,
                    rating = EXCLUDED.rating,
                    max_rating = EXCLUDED.max_rating,
                    badges = EXCLUDED.badges,
                    topic_stats = EXCLUDED.topic_stats,
                    updated_at = CURRENT_TIMESTAMP;
            """
            cursor.execute(query, (
                data["platform"],
                data["handle"],
                data["total_solved"],
                data["easy"],
                data["medium"],
                data["hard"],
                str(data.get("global_rank", data.get("rank", "N/A"))),
                data["rating"] if isinstance(data["rating"], int) else 0,
                str(data["max_rating"]),
                json.dumps(data.get("badges", [])),
                json.dumps(data.get("topics", []))
            ))
            conn.commit()
            cursor.close()
            conn.close()
    except Exception as db_err:
        print("Database save error:", db_err)

    return data


# -------------------------------------------------------------
# 3. UPCOMING CONTESTS SCHEDULE
# -------------------------------------------------------------
@app.get("/api/upcoming-contests")
def upcoming_contests():
    try:
        res = requests.get("https://kontests.net/api/v1/all", timeout=4).json()
        formatted = []
        for c in res[:6]:
            formatted.append({
                "name": c.get("name"),
                "platform": c.get("site", "Competitive"),
                "duration": f"{int(float(c.get('duration', 0)) // 3600)}h {int((float(c.get('duration', 0)) % 3600) // 60)}m",
                "url": c.get("url")
            })
        return formatted
    except Exception:
        return [
            {"name": "LeetCode Weekly Contest", "platform": "LeetCode", "duration": "1.5h", "url": "https://leetcode.com/contest/"},
            {"name": "Codeforces Round (Div. 2)", "platform": "Codeforces", "duration": "2.0h", "url": "https://codeforces.com/contests"},
            {"name": "CodeChef Starters", "platform": "CodeChef", "duration": "2.0h", "url": "https://www.codechef.com/contests"}
        ]