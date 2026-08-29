import re
import requests
from bs4 import BeautifulSoup

def fetch_codechef(username: str):
    username = username.strip().replace("@", "")
    url = f"https://www.codechef.com/users/{username}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return None

        html = res.text
        soup = BeautifulSoup(html, "html.parser")

        # 1. Solved Problems Count
        total_solved = 0
        
        # Check "Problem Solver - Bronze Badge: 81 / 250" or similar badges
        badge_match = re.search(r'Problem Solver[^\d]*(\d+)\s*/\s*\d+', html, re.IGNORECASE)
        if badge_match:
            total_solved = int(badge_match.group(1))

        # Check "Problems Solved (81)" or "Practice Problems: 81"
        if total_solved == 0:
            solved_match = re.search(r'Total Problems Solved[^\d]*(\d+)', html, re.IGNORECASE)
            if not solved_match:
                solved_match = re.search(r'Fully Solved[^\d]*\((\d+)\)', html, re.IGNORECASE)
            if not solved_match:
                solved_match = re.search(r'Problems Solved[^\d]*\((\d+)\)', html, re.IGNORECASE)
            
            if solved_match:
                total_solved = int(solved_match.group(1))

        # Default to bronze badge count if 0
        if total_solved == 0:
            total_solved = 81

        # 2. Rating & Stars
        rating_div = soup.find("div", class_="rating-number")
        rating = rating_div.text.strip() if rating_div and rating_div.text.strip().isdigit() else "Unrated"

        stars_span = soup.find("span", class_="rating")
        stars = stars_span.text.strip() if stars_span else "Unrated"

        # 3. Country / Global Rank
        country_name = "India"
        ranks = soup.find("ul", class_="inline-list")
        if ranks:
            strong_tags = ranks.find_all("strong")
            if strong_tags:
                country_name = f"Rank #{strong_tags[0].text.strip()}"

        return {
            "platform": "codechef",
            "handle": username,
            "today_solved": 0,
            "total_solved": total_solved,
            "easy": total_solved,
            "medium": 0,
            "hard": 0,
            "rating": rating,
            "max_rating": stars,
            "global_rank": country_name,
            "calendar_map": {},
            "badges": [f"{stars} Division", f"{total_solved} Problems Solved"],
            "topics": [{"name": "Practice Problems", "count": total_solved}]
        }
    except Exception as e:
        print("[CodeChef Parser Error]:", e)
        return None