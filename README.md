DSA Tracker (Performance Hub)


A centralized full-stack dashboard designed to track, aggregate, and analyze real-time competitive programming and coding metrics across multiple platforms including LeetCode, Codeforces, CodeChef, and GeeksforGeeks.

#Features:

1. Multi-Platform Telemetry: Aggregate stats (Total Solved, Easy/Medium/Hard breakdown, ratings, and ranks) from LeetCode, Codeforces, CodeChef, and GFG.

2. Upcoming Contests Schedule: Track live and upcoming competitive programming contests.

3. AI Roadmap & Doubts: Interactive chat assistant to clear DSA doubts and build problem-solving roadmaps.

4. Local Caching: Persistent browser-side data caching via localStorage.


#Tech Stack:

Backend: FastAPI, Python, Requests, BeautifulSoup4, Playwright

Frontend: Vanilla JavaScript, HTML5, Modern CSS3

Deployment: Render (Backend), Vercel (Frontend)


#project structure: 

dsa-tracker/
│
├── backend/
│   ├── services/
│   │   ├── codechef.py
│   │   ├── codeforces.py
│   │   ├── gfg.py
│   │   └── leetcode.py
│   ├── main.py
│   └── requirements.txt
│
└── frontend/
    ├── index.html
    ├── style.css
    └── app.js


#Local Installation & Setup:

1. Clone the Repository

git clone https://github.com/aradhyarast-hash/DSA-tracker-mvp.git
cd dsa-tracker

2. Backend Setup
Navigate to the backend directory and set up a virtual environment:

cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright binaries (required for web scraping services)
playwright install

# Run the FastAPI development server
uvicorn main:app --host 127.0.0.1 --port 8000 --reload


3. Frontend Setup

Open a separate terminal window and serve the frontend files using a live server (like Live Server extension in VS Code) or open frontend/index.html directly in your browser.
Ensure your frontend/app.js points to your local backend ([http://127.0.0.1:8000/api/fetch-stats](http://127.0.0.1:8000/api/fetch-stats)).


#API Endpoints:
1.
GET /api/fetch-stats?platform=<name>&username=<handle> - Fetches real-time telemetry for a specific platform.

2.
GET /api/upcoming-contests - Fetches the latest competitive programming contests schedule.

3.
POST /api/ai-chat - Interacts with the AI assistant backend.