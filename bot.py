import feedparser
import requests
import time

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1463918472760266782/b2ymrWV1vZrCWtdYY7B3ZhINMjiM3hZ1C6d4u1GQZ0bb_8khed9QA9XJjs4kJ202SK1J"

KEYWORDS = [
    "reddit task",
    "reddit marketing",
    "need reddit promotion"
]

sent_posts = set()

RSS_URL = "https://www.reddit.com/r/all/new/.rss"

def send_to_discord(title, link):
    data = {
        "content": f"🚨 New Match Found!\n\n📌 {title}\n🔗 {link}"
    }

    requests.post(DISCORD_WEBHOOK, json=data)

while True:
    try:
        feed = feedparser.parse(RSS_URL)

        for entry in feed.entries:

            title = entry.title.lower()

            if entry.link in sent_posts:
                continue

            for keyword in KEYWORDS:
                if keyword.lower() in title:

                    send_to_discord(entry.title, entry.link)

                    sent_posts.add(entry.link)

                    print("Found:", entry.title)

                    break

        time.sleep(30)

    except Exception as e:
        print(e)
        time.sleep(10)
