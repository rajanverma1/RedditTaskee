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

    # Reddit tasks
    "reddit task",
    "reddit tasks",
    "need reddit task",
    "reddit worker",
    "reddit work",
    "reddit posting",
    "reddit marketer",
    "reddit marketing",
    "reddit promotion",
    "reddit promoter",
    "reddit engagement",
    "reddit growth",
    "reddit boosting",
    "reddit campaign",
    "reddit management",
    "reddit manager",
    "reddit comments",
    "reddit upvotes",
    "reddit outreach",

    # Hiring style
    "looking for reddit",
    "need reddit help",
    "hiring reddit",
    "reddit freelancer",
    "reddit agency",
    "reddit expert",
    "reddit specialist",
    "reddit assistant",
    "reddit VA",
    "reddit traffic",

    # Promotion related
    "promote on reddit",
    "reddit advertising",
    "reddit ads",
    "grow on reddit",
    "reddit visibility",
    "reddit exposure",
    "subreddit promotion",
    "subreddit marketing",

    # Startup / SaaS
    "launch on reddit",
    "reddit launch",
    "startup promotion reddit",
    "saas reddit marketing",
    "reddit user acquisition",

    # Crypto / Web3
    "shill on reddit",
    "reddit shilling",
    "crypto reddit marketing",
    "token reddit promotion",

    # Comment related
    "need comments",
    "need engagement",
    "need upvotes",
    "boost my reddit post",

    # Misc
    "karma service",
    "karma growth",
    "reddit seo",
    "reddit outreach service"
]

# ==============================
# RSS URL
# ==============================

RSS_URL = "https://www.reddit.com/r/all/new/.rss"

# ==============================
# REQUEST HEADERS
# ==============================

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# ==============================
# SAVED POSTS
# ==============================

sent_posts = set()

# ==============================
# SEND TO DISCORD
# ==============================

def send_to_discord(title, link):

    message = {
        "content": f"""
🚨 NEW REDDIT LEAD FOUND

📌 Title:
{title}

🔗 Link:
{link}
"""
    }

    requests.post(DISCORD_WEBHOOK, json=message)

# ==============================
# BOT START
# ==============================

print("✅ Bot started successfully.")

# ==============================
# MAIN LOOP
# ==============================

while True:

    try:

        print("🔍 Checking Reddit...")

        response = requests.get(
            RSS_URL,
            headers=HEADERS
        )

        feed = feedparser.parse(response.text)

        for entry in feed.entries:

            title = entry.title.lower()

            print("📄", entry.title)

            # Skip duplicates
            if entry.link in sent_posts:
                continue

            # Keyword matching
            for keyword in KEYWORDS:

                if keyword.lower() in title:

                    print("🚨 Match Found:", entry.title)

                    send_to_discord(
                        entry.title,
                        entry.link
                    )

                    sent_posts.add(entry.link)

                    break

        print("⏳ Waiting 30 seconds...\n")

        time.sleep(30)

    except Exception as e:

        print("❌ ERROR:", e)

        time.sleep(15)
