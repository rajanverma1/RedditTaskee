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
# KEYWORDS
# ==============================

KEYWORDS = [
    "reddit task",
    "reddit marketing",
    "need reddit promotion",
    "reddit engagement"
]

# ==============================
# RSS URL
# ==============================

RSS_URL = "https://www.reddit.com/r/all/new/.rss"

# ==============================
# HEADERS
# ==============================

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# ==============================
# SAVED POSTS
# ==============================

sent_posts = set()

# ==============================
# DISCORD FUNCTION
# ==============================

def send_to_discord(title, link):

    data = {
        "content": f"""
🚨 New Reddit Lead Found!

📌 {title}

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

        response = requests.get(RSS_URL, headers=HEADERS)

        feed = feedparser.parse(response.text)

        for entry in feed.entries:

            print(entry.title)

            title = entry.title.lower()

            if entry.link in sent_posts:
                continue

            for keyword in KEYWORDS:

                if keyword.lower() in title:

                    send_to_discord(
                        entry.title,
                        entry.link
                    )

                    sent_posts.add(entry.link)

                    print("Keyword Found:", entry.title)

                    break

        time.sleep(30)

    except Exception as e:

        print("ERROR:", e)

        time.sleep(15)
