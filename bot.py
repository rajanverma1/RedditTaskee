import feedparser
import requests
import time
import re
import os
import json

# =====================================================
# DISCORD WEBHOOK
# =====================================================

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1463918472760266782/b2ymrWV1vZrCWtdYY7B3ZhINMjiM3hZ1C6d4u1GQZ0bb_8khed9QA9XJjs4kJ202SK1J"

# =====================================================
# PERSISTENCE FILE (survives restarts)
# =====================================================

SEEN_POSTS_FILE = "seen_posts.json"

def load_seen_posts():
    if os.path.exists(SEEN_POSTS_FILE):
        try:
            with open(SEEN_POSTS_FILE, "r") as f:
                return set(json.load(f))
        except Exception:
            pass
    return set()

def save_seen_posts(seen):
    try:
        with open(SEEN_POSTS_FILE, "w") as f:
            json.dump(list(seen), f)
    except Exception as e:
        print(f"⚠️ Could not save seen posts: {e}")

# =====================================================
# STARTUP MESSAGE
# =====================================================

def send_startup_message():
    try:
        response = requests.post(
            DISCORD_WEBHOOK,
            json={"content": "✅ Advanced Reddit Hiring Lead Monitor Started"},
            timeout=10
        )
        response.raise_for_status()
    except Exception as e:
        print(f"⚠️ Could not send startup message: {e}")

# =====================================================
# SUBREDDITS TO MONITOR
# =====================================================

SUBREDDITS = [
    "freelance_forhire",
    "forhire",
    "slavelabour",
    "jobs",
    "forhireindia",
    "startups",
    "entrepreneur",
    "smallbusiness",
    "sideproject",
    "marketing",
    "hiring",
    "remotejobs"
]

# =====================================================
# KEYWORDS
# =====================================================

KEYWORDS = [
    # Hiring tags
    "[hiring]", "[hire]", "[for hire]", "[task]", "[job]",
    # Hiring words
    "hiring", "hire", "looking for", "need workers", "need people",
    "looking to hire", "job offer", "remote work", "work from home",
    # Reddit work
    "reddit task", "reddit tasks", "reddit work", "reddit posting",
    "reddit comments", "reddit engagement", "reddit promotion",
    "reddit marketing", "reddit growth", "reddit upvotes",
    "subreddit promotion",
    # Engagement work
    "commenting", "basic engagement", "social engagement",
    "need engagement", "boost post", "promote post",
    # Payment words
    "paid", "earn", "salary", "weekly pay", "payment",
    "extra income", "side income",
    # Contact
    "telegram", "discord", "dm me", "message me", "interested comment",
]

# =====================================================
# REQUEST HEADERS
# =====================================================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; HiringMonitor/1.0)"
}

# =====================================================
# TELEGRAM DETECTION
# =====================================================

def extract_telegram(text):
    # Require @ or t.me/ prefix to reduce false positives
    pattern = r"(?:t\.me/|telegram[:\s]+@?)([a-zA-Z0-9_]{5,32})"
    matches = re.findall(pattern, text, re.IGNORECASE)
    return matches[0] if matches else "Not Found"

# =====================================================
# DISCORD DETECTION
# =====================================================

def extract_discord(text):
    # Match username#1234 format or discord.gg/ links
    pattern = r"(?:discord\.gg/([a-zA-Z0-9]+)|discord[:\s]+([a-zA-Z0-9_.]{2,32}#\d{4}))"
    matches = re.findall(pattern, text, re.IGNORECASE)
    if matches:
        # Return first non-empty group
        return next((g for m in matches for g in m if g), "Not Found")
    return "Not Found"

# =====================================================
# LEAD SCORING
# =====================================================

SCORE_WORDS = [
    "hiring", "hire", "reddit", "engagement",
    "promotion", "paid", "worker", "task", "comment", "marketing"
]

MAX_SCORE = len(SCORE_WORDS)  # 10

def calculate_score(text):
    lower = text.lower()
    return sum(1 for word in SCORE_WORDS if word in lower)

# =====================================================
# SEND TO DISCORD
# =====================================================

def send_to_discord(title, link, subreddit, score, telegram, discord_user):
    message = {
        "content": (
            f"🚨 **NEW REDDIT LEAD FOUND**\n\n"
            f"📂 **Subreddit:** r/{subreddit}\n"
            f"📌 **Title:** {title}\n"
            f"🔥 **Lead Score:** {score}/{MAX_SCORE}\n"
            f"📲 **Telegram:** {telegram}\n"
            f"💬 **Discord:** {discord_user}\n"
            f"🔗 **Link:** {link}"
        )
    }
    try:
        response = requests.post(DISCORD_WEBHOOK, json=message, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"⚠️ Failed to send Discord message: {e}")

# =====================================================
# CHECK SUBREDDIT
# =====================================================

def check_subreddit(subreddit, seen_posts):
    rss_url = f"https://www.reddit.com/r/{subreddit}/new/.rss"

    try:
        response = requests.get(rss_url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"⚠️ Could not fetch r/{subreddit}: {e}")
        return

    feed = feedparser.parse(response.text)

    entries = getattr(feed, "entries", [])
    if not entries:
        print(f"⚠️ No entries found for r/{subreddit}")
        return

    for entry in entries:
        title = getattr(entry, "title", "").strip()
        link = getattr(entry, "link", "")

        if not title or not link:
            continue

        # Skip duplicates
        if link in seen_posts:
            continue

        lower_title = title.lower()
        matched = any(kw.lower() in lower_title for kw in KEYWORDS)

        if not matched:
            continue

        score = calculate_score(title)

        # Filter weak leads
        if score < 2:
            continue

        print(f"🚨 MATCH FOUND: {title}")

        telegram = extract_telegram(title)
        discord_user = extract_discord(title)

        send_to_discord(title, link, subreddit, score, telegram, discord_user)

        seen_posts.add(link)

    # Trim seen_posts to last 5000 to avoid unbounded growth
    if len(seen_posts) > 5000:
        trimmed = list(seen_posts)[-5000:]
        seen_posts.clear()
        seen_posts.update(trimmed)

# =====================================================
# MAIN
# =====================================================

print("✅ Advanced Reddit Hiring Monitor Running")
send_startup_message()

seen_posts = load_seen_posts()

while True:
    try:
        print("🔍 Scanning Reddit...")

        for subreddit in SUBREDDITS:
            print(f"📂 Checking r/{subreddit}")
            check_subreddit(subreddit, seen_posts)
            time.sleep(2)  # Polite delay between requests

        save_seen_posts(seen_posts)
        print("⏳ Waiting 30 seconds...\n")
        time.sleep(30)

    except Exception as e:
        print(f"❌ ERROR: {e}")
        time.sleep(15)
