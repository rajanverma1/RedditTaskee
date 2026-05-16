import feedparser
import requests
import time

# ==============================
# DISCORD WEBHOOK
# ==============================

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1463918472760266782/b2ymrWV1vZrCWtdYY7B3ZhINMjiM3hZ1C6d4u1GQZ0bb_8khed9QA9XJjs4kJ202SK1J"

# ==============================
# STARTUP MESSAGE
# ==============================

requests.post(DISCORD_WEBHOOK, json={
    "content": "✅ Reddit monitor bot started successfully."
})

# ==============================
# KEYWORDS TO TRACK
# ==============================

KEYWORDS = [
    "reddit task",
    "reddit marketing",
    "need reddit promotion",
    "reddit engagement"
]

# ==============================
# RSS FEED
# ==============================

RSS_URL = "https://www.reddit.com/r/all/new/.rss"

# ==============================
# TRACKED POSTS
# ==============================

sent_posts = set()

# ==============================
# SEND ALERT FUNCTION
# ==============================

def send_to_discord(title, link):
    data = {
        "content": f"""
🚨 New Reddit Lead Found!

📌 Title: {title}

🔗 {link}
"""
    }

    requests.post(DISCORD_WEBHOOK, json=data)

# ==============================
# BOT LOOP
# ==============================

print("Bot started...")

while True:
    try:

        print("Checking Reddit...")

        feed = feedparser.parse(RSS_URL)

        for entry in feed.entries:

            title = entry.title.lower()

            print("Post:", entry.title)

            if entry.link in sent_posts:
                continue

            for keyword in KEY
