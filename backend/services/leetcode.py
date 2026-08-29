import json
import requests
from datetime import datetime, timezone

def fetch_leetcode(username: str):
    username = username.strip().replace("@", "")
    url = "https://leetcode.com/graphql"
    
    query = """
    query userProfile($username: String!) {
      matchedUser(username: $username) {
        submitStats: submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
        profile {
          ranking
          reputation
        }
        userCalendar {
          submissionCalendar
        }
        tagProblemCounts {
          fundamental { tagName problemsSolved }
          intermediate { tagName problemsSolved }
          advanced { tagName problemsSolved }
        }
      }
      userContestRanking(username: $username) {
        rating
        globalRanking
        topPercentage
      }
    }
    """
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": f"https://leetcode.com/{username}/",
        "Content-Type": "application/json"
    }
    
    try:
        res = requests.post(url, json={"query": query, "variables": {"username": username}}, headers=headers, timeout=10)
        data = res.json().get("data", {})
        matched_user = data.get("matchedUser")
        
        if not matched_user:
            return None
            
        stats = {x["difficulty"]: x["count"] for x in matched_user["submitStats"]["acSubmissionNum"]}
        
        # Parse Calendar
        raw_cal = matched_user.get("userCalendar", {}).get("submissionCalendar") or "{}"
        cal_data = json.loads(raw_cal) if isinstance(raw_cal, str) else raw_cal
        calendar_map = {}
        today_solved = 0
        today_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        
        for ts, count in cal_data.items():
            dt = datetime.fromtimestamp(int(ts), tz=timezone.utc).strftime('%Y-%m-%d')
            calendar_map[dt] = calendar_map.get(dt, 0) + int(count)
            if dt == today_str:
                today_solved += int(count)

        # Parse Contest
        contest = data.get("userContestRanking") or {}
        rating = int(round(contest.get("rating", 0)))
        rank = matched_user["profile"].get("ranking", "N/A")
        
        # Parse Topics
        tag_data = matched_user.get("tagProblemCounts", {})
        all_tags = tag_data.get("fundamental", []) + tag_data.get("intermediate", []) + tag_data.get("advanced", [])
        sorted_topics = [{"name": t["tagName"], "count": t["problemsSolved"]} for t in all_tags if t["problemsSolved"] > 0][:10]
        
        return {
            "platform": "leetcode",
            "handle": username,
            "today_solved": today_solved,
            "total_solved": stats.get("All", 0),
            "easy": stats.get("Easy", 0),
            "medium": stats.get("Medium", 0),
            "hard": stats.get("Hard", 0),
            "rating": rating if rating > 0 else "--",
            "max_rating": f"Top {contest.get('topPercentage')}%" if contest.get("topPercentage") else "--",
            "global_rank": f"Rank #{rank}" if rank != "N/A" else "Unranked",
            "calendar_map": calendar_map,
            "badges": ["LeetCode Active Solver", f"{stats.get('All', 0)} Solved"],
            "topics": sorted_topics if sorted_topics else [{"name": "General DSA", "count": stats.get("All", 0)}]
        }
    except Exception as e:
        print("[LeetCode Error]:", e)
        return None