let activePlatform = 'overview';
const API_BASE = "http://127.0.0.1:8000/api/fetch-stats";
const CONTESTS_API = "http://127.0.0.1:8000/api/upcoming-contests";
const AI_CHAT_API = "http://127.0.0.1:8000/api/ai-chat";

const ALL_PLATFORMS = ['leetcode', 'codeforces', 'codechef', 'gfg'];

function getSavedPlatformData(platform) {
  const data = localStorage.getItem(`dsa_tracker_${platform}`);
  return data ? JSON.parse(data) : null;
}

function savePlatformData(platform, data, username) {
  localStorage.setItem(`dsa_tracker_${platform}`, JSON.stringify(data));
  localStorage.setItem(`dsa_tracker_${platform}_handle`, username);
}

function resetDashboardUI() {
  document.getElementById("today-solved-val").innerText = "--";
  document.getElementById("total-solved-val").innerText = "--";
  document.getElementById("easy-val").innerText = "--";
  document.getElementById("med-val").innerText = "--";
  document.getElementById("hard-val").innerText = "--";
  document.getElementById("global-rank-val").innerText = "Global Rank: --";
  document.getElementById("rating-val").innerText = "--";
  document.getElementById("max-rating-val").innerText = "Max: --";

  document.getElementById("topic-tags-container").innerHTML = `<span class="tag">Sync profile to load topics</span>`;
  document.getElementById("badge-container").innerHTML = `
    <div class="badge-item">
      <span class="badge-icon">🛡️</span>
      <div><strong>No Badges Synced</strong><p>Sync to load</p></div>
    </div>`;
}

// 1. Overview Dashboard
function renderOverviewDashboard() {
  let totalSolved = 0;
  let todaySolved = 0;
  let easySolved = 0;
  let medSolved = 0;
  let hardSolved = 0;
  let allTopics = [];
  let allBadges = [];
  let connectedCount = 0;

  ALL_PLATFORMS.forEach(p => {
    const data = getSavedPlatformData(p);
    if (data) {
      connectedCount++;
      totalSolved += Number(data.total_solved) || 0;
      todaySolved += Number(data.today_solved) || 0;
      easySolved += Number(data.easy) || 0;
      medSolved += Number(data.medium) || 0;
      hardSolved += Number(data.hard) || 0;

      if (data.topics) allTopics.push(...data.topics);
      if (data.badges) allBadges.push(...data.badges);
    }
  });

  document.getElementById("current-platform-title").innerText = "All Platforms Overview";
  const syncBar = document.querySelector(".sync-bar");
  if (syncBar) syncBar.style.display = "none";

  if (connectedCount === 0) {
    resetDashboardUI();
    return;
  }

  document.getElementById("today-solved-val").innerText = todaySolved;
  document.getElementById("total-solved-val").innerText = totalSolved;
  document.getElementById("easy-val").innerText = easySolved;
  document.getElementById("med-val").innerText = medSolved;
  document.getElementById("hard-val").innerText = hardSolved;
  document.getElementById("global-rank-val").innerText = `${connectedCount} Connected Platform(s)`;
  document.getElementById("rating-val").innerText = "Aggregated";
  document.getElementById("max-rating-val").innerText = `Total: ${totalSolved} Qs`;

  const topicBox = document.getElementById("topic-tags-container");
  if (allTopics.length > 0) {
    topicBox.innerHTML = allTopics.slice(0, 10).map(t => `<span class="tag">${t.name} (${t.count})</span>`).join('');
  } else {
    topicBox.innerHTML = `<span class="tag">No topics recorded</span>`;
  }

  const badgeBox = document.getElementById("badge-container");
  if (allBadges.length > 0) {
    badgeBox.innerHTML = allBadges.slice(0, 4).map(b => `
      <div class="badge-item">
        <span class="badge-icon">🏅</span>
        <div><strong>${b}</strong><p>Verified</p></div>
      </div>
    `).join('');
  }
}

// 2. Display Platform Data
function displayPlatformData(data) {
  const syncBar = document.querySelector(".sync-bar");
  if (syncBar) syncBar.style.display = "flex";

  document.getElementById("today-solved-val").innerText = data.today_solved ?? 0;
  document.getElementById("total-solved-val").innerText = data.total_solved ?? 0;
  document.getElementById("easy-val").innerText = data.easy ?? 0;
  document.getElementById("med-val").innerText = data.medium ?? 0;
  document.getElementById("hard-val").innerText = data.hard ?? 0;
  document.getElementById("global-rank-val").innerText = data.global_rank || 'N/A';
  document.getElementById("rating-val").innerText = data.rating ?? '--';
  document.getElementById("max-rating-val").innerText = data.max_rating || '--';

  const topicBox = document.getElementById("topic-tags-container");
  if (data.topics && data.topics.length > 0) {
    topicBox.innerHTML = data.topics.map(t => `<span class="tag">${t.name} (${t.count})</span>`).join('');
  } else {
    topicBox.innerHTML = `<span class="tag">No topics recorded</span>`;
  }

  const badgeBox = document.getElementById("badge-container");
  if (data.badges && data.badges.length > 0) {
    badgeBox.innerHTML = data.badges.map(b => `
      <div class="badge-item">
        <span class="badge-icon">🏅</span>
        <div><strong>${b}</strong><p>Verified</p></div>
      </div>
    `).join('');
  } else {
    badgeBox.innerHTML = `<span class="tag">No badges</span>`;
  }
}

// 3. Platform Switch
function switchPlatform(platform, element) {
  activePlatform = platform;
  
  document.querySelectorAll(".platform-nav .nav-item").forEach(btn => btn.classList.remove("active"));
  if (element) element.classList.add("active");

  document.getElementById("analytics-view").style.display = "block";
  document.getElementById("ai-chat-view").style.display = "none";

  if (platform === 'overview') {
    renderOverviewDashboard();
    return;
  }

  const titles = {
    leetcode: "LeetCode Dashboard",
    codeforces: "Codeforces Dashboard",
    codechef: "CodeChef Dashboard",
    gfg: "GeeksforGeeks Dashboard"
  };
  
  document.getElementById("current-platform-title").innerText = titles[platform] || "Platform Dashboard";
  const syncBar = document.querySelector(".sync-bar");
  if (syncBar) syncBar.style.display = "flex";

  const savedHandle = localStorage.getItem(`dsa_tracker_${platform}_handle`) || "";
  document.getElementById("platform-handle-input").value = savedHandle;
  document.getElementById("platform-handle-input").placeholder = `Enter ${platform.toUpperCase()} username...`;

  const savedData = getSavedPlatformData(platform);
  if (savedData) {
    displayPlatformData(savedData);
  } else {
    resetDashboardUI();
  }
}

// 4. Sync Profile
async function syncCurrentPlatform() {
  if (activePlatform === 'overview') return;

  const rawInput = document.getElementById("platform-handle-input").value.trim();
  const btn = document.getElementById("sync-btn");

  if (!rawInput) {
    alert("Please enter a username!");
    return;
  }

  let username = rawInput.replace(/\/+$/, "").split("/").pop().replace("@", "").trim();

  btn.innerText = "Syncing...";
  btn.disabled = true;

  try {
    const targetUrl = `${API_BASE}?platform=${encodeURIComponent(activePlatform)}&username=${encodeURIComponent(username)}`;
    const res = await fetch(targetUrl);
    const data = await res.json();

    if (!res.ok) {
      alert(data.detail || `User "${username}" not found on ${activePlatform}.`);
      return;
    }

    savePlatformData(activePlatform, data, username);
    document.getElementById("user-display-handle").innerText = `@${username}`;
    displayPlatformData(data);

  } catch (err) {
    console.error("Fetch failure:", err);
    alert("Could not connect to backend server at 127.0.0.1:8000.");
  } finally {
    btn.innerText = "Sync Profile";
    btn.disabled = false;
  }
}

// 5. Contests
async function loadUpcomingContests() {
  const container = document.getElementById("contest-list-container");
  if (!container) return;

  try {
    const res = await fetch(CONTESTS_API);
    const contests = await res.json();
    
    if (contests && contests.length > 0) {
      container.innerHTML = contests.map(c => `
        <div class="contest-card">
          <div class="contest-info">
            <strong>${c.name}</strong>
            <span>Platform: ${c.platform} • Duration: ${c.duration}</span>
          </div>
          <a href="${c.url}" target="_blank" class="btn-register" style="text-decoration:none; display:inline-block;">Open Contest</a>
        </div>
      `).join('');
    }
  } catch (e) {
    console.log("Contests load deferred:", e);
  }
}

// 6. Logout
function logoutUser() {
  if (confirm("Clear all synced platform data?")) {
    ALL_PLATFORMS.forEach(p => {
      localStorage.removeItem(`dsa_tracker_${p}`);
      localStorage.removeItem(`dsa_tracker_${p}_handle`);
    });
    document.getElementById("platform-handle-input").value = "";
    document.getElementById("user-display-handle").innerText = "@no_session";
    switchPlatform('overview', document.querySelector(".platform-nav .nav-item"));
  }
}

// 7. AI Chatbot View
function openAiChatbot() {
  document.querySelectorAll(".platform-nav .nav-item").forEach(btn => btn.classList.remove("active"));
  document.getElementById("analytics-view").style.display = "none";
  document.getElementById("ai-chat-view").style.display = "block";
}

async function sendChatMessage() {
  const input = document.getElementById("chat-input");
  const text = input.value.trim();
  if (!text) return;

  const chatContainer = document.getElementById("chat-messages");
  const userBubble = document.createElement("div");
  userBubble.className = "chat-msg user";
  userBubble.innerText = text;
  chatContainer.appendChild(userBubble);
  input.value = "";

  const aiBubble = document.createElement("div");
  aiBubble.className = "chat-msg ai";
  aiBubble.innerHTML = "<em>Thinking...</em>";
  chatContainer.appendChild(aiBubble);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  try {
    const res = await fetch(AI_CHAT_API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    aiBubble.innerHTML = data.reply
      .replace(/\n\n/g, '<br><br>')
      .replace(/\n/g, '<br>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  } catch (err) {
    aiBubble.innerHTML = "⚠️ Could not reach AI service.";
  } finally {
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }
}

function handleChatEnter(e) {
  if (e.key === "Enter") sendChatMessage();
}

window.addEventListener("DOMContentLoaded", () => {
  switchPlatform('overview', document.querySelector(".platform-nav .nav-item"));
  loadUpcomingContests();
});