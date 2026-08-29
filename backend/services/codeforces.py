import requests
from datetime import datetime, timezone

def fetch_codeforces(handle: str):
    handle = handle.strip().replace("@", "")
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        # 1. User Info
        info_res = requests.get(f"https://codeforces.com/api/user.info?handles={handle}", headers=headers, timeout=8).json()
        if info_res.get("status") != "OK" or not info_res.get("result"):
            return None
        user = info_res["result"][0]
        
        # 2. Submissions
        status_res = requests.get(f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=1000", headers=headers, timeout=10).json()
        
        solved_set = set()
        calendar_map = {}
        topic_counts = {}
        today_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        today_solved = 0
        
        easy_cnt = 0
        med_cnt = 0
        hard_cnt = 0
        
        if status_res.get("status") == "OK":
            for sub in status_res.get("result", []):
                if sub.get("verdict") == "OK":
                    prob = sub.get("problem", {})
                    pid = f"{prob.get('contestId')}-{prob.get('index')}"
                    
                    if pid not in solved_set:
                        solved_set.add(pid)
                        r = prob.get("rating", 800)
                        if r < 1200: easy_cnt += 1
                        elif r < 1600: med_cnt += 1
                        else: hard_cnt += 1
                        
                        for tag in prob.get("tags", []):
                            t_title = tag.title()
                            topic_counts[t_title] = topic_counts.get(t_title, 0) + 1
                    
                    ts = sub.get("creationTimeSeconds", 0)
                    dt = datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%Y-%m-%d')
                    calendar_map[dt] = calendar_map.get(dt, 0) + 1
                    if dt == today_str:
                        today_solved += 1

        total_solved = len(solved_set)
        sorted_topics = [{"name": k, "count": v} for k, v in sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:8]]

        return {
            "platform": "codeforces",
            "handle": handle,
            "today_solved": today_solved,
            "total_solved": total_solved,
            "easy": easy_cnt,
            "medium": med_cnt,
            "hard": hard_cnt,
            "rating": user.get("rating", "--"),
            "max_rating": f"Max: {user.get('maxRating', '--')}",
            "global_rank": user.get("rank", "Unrated").capitalize(),
            "calendar_map": calendar_map,
            "badges": [user.get("rank", "Participant").capitalize(), f"Rating: {user.get('rating', 0)}"],
            "topics": sorted_topics
        }
    except Exception as e:
        print("[Codeforces Error]:", e)
        return None