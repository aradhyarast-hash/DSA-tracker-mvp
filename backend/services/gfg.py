import re
import requests
from bs4 import BeautifulSoup

def fetch_gfg(username_or_url: str):
    raw = username_or_url.strip().strip("/")
    
    # URL se clean handle nikalna (chahe /user/ ho ya /profile/ ho)
    if "geeksforgeeks.org" in raw:
        parts = raw.split("/")
        clean_handle = parts[-1].split("?")[0] if parts else raw
    else:
        clean_handle = raw.replace("@", "").split("?")[0]

    url = f"https://www.geeksforgeeks.org/user/{clean_handle}/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.geeksforgeeks.org/"
    }

    try:
        res = requests.get(url, headers=headers, timeout=12)
        if res.status_code != 200:
            print(f"[GFG HTML Error]: Status code {res.status_code}")
            return None

        html = res.text
        soup = BeautifulSoup(html, "html.parser")

        # 1. Text search via Regex on entire HTML body for Problem Solved
        total_solved = 0
        
        # GFG ke page par "Problems Solved: X" ya similar pattern search karte hain
        patterns = [
            r'total[_\s-]?problems[_\s-]?solved[^\d]*(\d+)',
            r'Problem[s]? Solved[^\d]*(\d+)',
            r'(\d+)\s*Problem[s]? Solved',
            r'Coding Score[^\d]*(\d+)'
        ]
        
        for pat in patterns:
            match = re.search(pat, html, re.IGNORECASE)
            if match:
                val = int(match.group(1))
                if "solved" in pat.lower() and val > 0:
                    total_solved = val
                    break

        # 2. Agar regex se total solved na mile, toh soup se div classes dhoondte hain
        if total_solved == 0:
            for div in soup.find_all(["div", "span", "card"]):
                text = div.get_text()
                if "Problems Solved" in text:
                    nums = re.findall(r'\d+', text)
                    if nums:
                        total_solved = int(nums[0])
                        break

        # 3. Coding Score nikalna
        score = 0
        score_match = re.search(r'Coding Score[^\d]*(\d+)', html, re.IGNORECASE)
        if score_match:
            score = int(score_match.group(1))

        # 4. Institute / College Name
        college = "Campus Coder"
        institute_div = soup.find(class_=re.compile("institute", re.I))
        if institute_div:
            college = institute_div.get_text().strip()

        # Fallback values agar profile empty ya protected ho
        if total_solved == 0 and score > 0:
            total_solved = score // 10 

        return {
            "platform": "gfg",
            "handle": clean_handle,
            "today_solved": 0,
            "total_solved": total_solved,
            "easy": total_solved,
            "medium": 0,
            "hard": 0,
            "rating": score,
            "max_rating": f"Score: {score}",
            "global_rank": f"Institute: {college}",
            "calendar_map": {},
            "badges": [f"GFG Solver ({total_solved})", f"Score: {score}"],
            "topics": [{"name": "DSA Practice", "count": total_solved}]
        }
    except Exception as e:
        print(f"[GFG Scraper Exception]: {e}")
        return None