import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from match import check_titles
from logger import get_logger

log = get_logger()

# Environment variables
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID", "UChz9nfVNmUiZryQtekbzS5g")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://notify.lunasea.app/v1/custom/device/dWFR0uxJKUElvsW_u981XT:APA91bFRz5Jb9QE5TkXqFa8RkKDOKFIQFkjdjXCRFCs9SUhi7kTDQA7EzqTsALu09H9PFz5L7l4YEpijwcc3eXqrmmrJjYwsGF2dyVjFwlFE3mBLNk1JH7Xt2hpyT01Mu1PU80AecvSK")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 5))  # Minutes
VIDEO_TITLE = os.getenv(
    "VIDEO_TITLE", "Zvezde Granda - Cela Emisija"
)  # Default title

# Construct the feed URL using the YouTube channel ID
YOUTUBE_FEED_URL = (
    f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}"
)


# Function to check if a video is published today
def is_video_today(published_date):
    today = datetime.now().date()
    return published_date.date() == today


# Function to send webhook notification
def send_webhook_notification(title, link):
    log.info("Sending webhook notification...")
    # Construct the payload for the webhook
    payload = json.dumps(
        {
            "title": "New Video!",
            "body": f"{title} uploaded a new episode.",
            "image": f"https://i4.ytimg.com/vi/{link}/hqdefault.jpg",  # YouTube thumbnail URL
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
            send_webhook_notification(title, link)


# Main loop
def main():
    while True:
        log.info(f"Checking {VIDEO_TITLE} for new videos in {YOUTUBE_FEED_URL}")
        check_youtube_feed()
        log.info(f"😴 Sleeping for {CHECK_INTERVAL} minutes...")
        time.sleep(CHECK_INTERVAL * 60)


if __name__ == "__main__":
    main()
