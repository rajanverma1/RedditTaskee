import feedparser
import requests
import time
import re

# =====================================================
# DISCORD WEBHOOK
# =====================================================

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1463918472760266782/b2ymrWV1vZrCWtdYY7B3ZhINMjiM3hZ1C6d4u1GQZ0bb_8khed9QA9XJjs4kJ202SK1J"

# =====================================================
# STARTUP MESSAGE
# =====================================================

requests.post(DISCORD_WEBHOOK, json={
    "content": "✅ Advanced Reddit Hiring Lead Monitor Started"
})

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
    "[hiring]",
    "[hire]",
    "[for hire]",
    "[task]",
    "[job]",

    # Hiring words
    "hiring",
    "hire",
    "looking for",
    "need workers",
    "need people",
    "looking to hire",
    "job offer",
    "remote work",
    "work from home",

    # Reddit work
    "reddit task",
    "reddit tasks",
    "reddit work",
    "reddit posting",
    "reddit comments",
    "reddit engagement",
    "reddit promotion",
    "reddit marketing",
    "reddit growth",
    "reddit upvotes",
    "subreddit promotion",

    # Engagement work
    "commenting",
    "basic engagement",
    "social engagement",
    "need engagement",
    "boost post",
    "promote post",

    # Payment words
    "paid",
    "earn",
    "salary",
    "weekly pay",
    "payment",
    "extra income",
    "side income",

    # Contact
    "telegram",
    "discord",
    "dm me",
    "message me",
    "interested comment",
]

# =====================================================
# REQUEST HEADERS
# =====================================================

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# =====================================================
# SAVED POSTS
# =====================================================

sent_posts = set()

# =====================================================
# TELEGRAM DETECTION
# =====================================================

def extract_telegram(text):

    telegram_pattern = r"(?:telegram|tg)[-:\\s]*@?([a-zA-Z0-9_]+)"

    matches = re.findall(
        telegram_pattern,
        text,
        re.IGNORECASE
    )

    if matches:
        return matches[0]

    return "Not Found"

# =====================================================
# DISCORD DETECTION
# =====================================================

def extract_discord(text):

    discord_pattern = r"(?:discord)[-:\\s]*@?([a-zA-Z0-9_.]+)"

    matches = re.findall(
        discord_pattern,
        text,
        re.IGNORECASE
    )

    if matches:
        return matches[0]

    return "Not Found"

# =====================================================
# LEAD SCORING
# =====================================================

def calculate_score(text):

    score = 0

    important_words = [

        "hiring",
        "hire",
        "reddit",
        "engagement",
        "promotion",
        "paid",
        "worker",
        "task",
        "comment",
        "marketing"
    ]

    for word in important_words:

        if word.lower() in text.lower():
            score += 1

    return score

# =====================================================
# SEND TO DISCORD
# =====================================================

def send_to_discord(
    title,
    link,
    subreddit,
    score,
    telegram,
    discord
):

    message = {
        "content": f"""
🚨 NEW REDDIT LEAD FOUND

📂 Subreddit:
r/{subreddit}

📌 Title:
{title}

🔥 Lead Score:
{score}/10

📲 Telegram:
{telegram}

💬 Discord:
{discord}

🔗 Link:
{link}
"""
    }

    requests.post(
        DISCORD_WEBHOOK,
        json=message
    )

# =====================================================
# CHECK SUBREDDIT
# =====================================================

def check_subreddit(subreddit):

    rss_url = f"https://www.reddit.com/r/{subreddit}/new/.rss"

    response = requests.get(
        rss_url,
        headers=HEADERS,
        timeout=15
    )

    feed = feedparser.parse(response.text)

    for entry in feed.entries:

        title = entry.title

        lower_title = title.lower()

        # Skip duplicates
        if entry.link in sent_posts:
            continue

        matched = False

        # Detect hiring titles instantly
        if "[hiring]" in lower_title:
            matched = True

        # Keyword detection
        for keyword in KEYWORDS:

            if keyword.lower() in lower_title:
                matched = True
                break

        # Ignore weak leads
        if matched:

            score = calculate_score(title)

            if score < 2:
                continue

            print("🚨 MATCH FOUND:", title)

            telegram = extract_telegram(title)

            discord = extract_discord(title)

            send_to_discord(
                title,
                entry.link,
                subreddit,
                score,
                telegram,
                discord
            )

            sent_posts.add(entry.link)

# =====================================================
# BOT START
# =====================================================

print("✅ Advanced Reddit Hiring Monitor Running")

# =====================================================
# MAIN LOOP
# =====================================================

while True:

    try:

        print("🔍 Scanning Reddit...")

        for subreddit in SUBREDDITS:

            print(f"📂 Checking r/{subreddit}")

            check_subreddit(subreddit)

        print("⏳ Waiting 30 seconds...\n")

        time.sleep(30)

    except Exception as e:

        print("❌ ERROR:", e)

        time.sleep(15)
