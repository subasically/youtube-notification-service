import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from match import check_titles
from logger import get_logger
import sys

log = get_logger()

# Environment variables
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 5))  # Minutes
VIDEO_TITLE = os.getenv("VIDEO_TITLE")  # Default title

if not YOUTUBE_CHANNEL_ID:
    log.error("Missing YOUTUBE_CHANNEL_ID environment variable.")
    sys.exit(1)

if not WEBHOOK_URL:
    log.error("Missing WEBHOOK_URL environment variable.")
    sys.exit(1)

if not VIDEO_TITLE:
    log.warning("Missing VIDEO_TITLE environment variable.")
    sys.exit(1)

# Construct the feed URL using the YouTube channel ID
YOUTUBE_FEED_URL = (
    f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}"
)


# Function to check if a video is published today
def is_video_today(published_date):
    today = datetime.now().date()
    return published_date.date() == today


# Function to send webhook notification
def send_webhook_notification(title, message, link):
    log.info("Sending webhook notification...")
    # Construct the payload for the webhook
    if link:
        payload = json.dumps(
            {
                "title": f"{title}",
                "body": f"{message}",
                "image": f"https://i4.ytimg.com/vi/{link}/hqdefault.jpg",  # YouTube thumbnail URL
            }
        )
    else:
        payload = json.dumps(
            {
                "title": f"{title}",
                "body": f"{message}",
                "image": "https://cdn-icons-png.flaticon.com/512/1384/1384060.png"
            }
        )

    headers = {"Content-Type": "application/json"}

    # Send the POST request to the webhook URL
    response = requests.post(WEBHOOK_URL, headers=headers, data=payload)

    log.info(f"Webhook sent. Response: {response.text}")


# Function to fetch and parse YouTube feed
def check_youtube_feed():
    response = requests.get(YOUTUBE_FEED_URL)
    soup = BeautifulSoup(response.text, "xml")

    for entry in soup.find_all("entry"):
        title = entry.title.text
        link = entry.link["href"].split("/")[-1]  # Extract the video ID from the link
        published_date = datetime.strptime(entry.published.text, "%Y-%m-%dT%H:%M:%S%z")

        # Use check_titles to validate the title
        log.info(f"Checking title: {title}")
        results = check_titles([title])
        if any(r.startswith("✅") for r in results) and is_video_today(published_date):
            log.info(f"New video found: {title}")
            send_webhook_notification(title, f"New video uploaded 😃😄‼️", link)


# Main loop
def main():
    # Send a startup notification
    log.info("Service starting up...")
    send_webhook_notification("Youtube Notification Service", "Startup Notification 👍", None)

    while True:
        log.info(f"Checking {VIDEO_TITLE} for new videos in {YOUTUBE_FEED_URL}")
        check_youtube_feed()
        log.info(f"😴 Sleeping for {CHECK_INTERVAL} minutes...")
        time.sleep(CHECK_INTERVAL * 60)


if __name__ == "__main__":
    main()
