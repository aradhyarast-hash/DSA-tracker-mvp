from .leetcode import fetch_leetcode
from .codeforces import fetch_codeforces
from .codechef import fetch_codechef
from .gfg import fetch_gfg

def get_platform_data(platform: str, username: str):
    p = platform.strip().lower()
    if p == "leetcode":
        return fetch_leetcode(username)
    elif p == "codeforces":
        return fetch_codeforces(username)
    elif p in ["codechef", "chef"]:
        return fetch_codechef(username)
    elif p in ["gfg", "geeksforgeeks"]:
        return fetch_gfg(username)
    return None