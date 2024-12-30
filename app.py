import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

# Environment variables
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 5))  # Minutes
NOTIFY_TITLE = os.getenv(
    "NOTIFY_TITLE", "Zvezde Granda - Cela Emisija"
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

    print(f"Webhook sent. Response: {response.text}")


# Function to fetch and parse YouTube feed
def check_youtube_feed():
    response = requests.get(YOUTUBE_FEED_URL)
    soup = BeautifulSoup(response.text, "xml")

    for entry in soup.find_all("entry"):
        title = entry.title.text
        link = entry.link["href"].split("/")[-1]  # Extract the video ID from the link
        published_date = datetime.strptime(entry.published.text, "%Y-%m-%dT%H:%M:%S%z")

        # Check if title matches and the video was published today
        if title == NOTIFY_TITLE and is_video_today(published_date):
            send_webhook_notification(title, link)


# Main loop
def main():
    while True:
        check_youtube_feed()
        time.sleep(CHECK_INTERVAL * 60)  # Sleep for the specified interval


if __name__ == "__main__":
    main()
