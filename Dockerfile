# Use Python 3.9 image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Set the environment variables
ENV YOUTUBE_FEED_URL="https://www.youtube.com/feeds/videos.xml?channel_id=YOUR_CHANNEL_ID"
ENV MQTT_BROKER="mqtt_broker"
ENV MQTT_TOPIC="youtube/notifications"
ENV MQTT_CLIENT_ID="youtube_notifier"
ENV MQTT_USERNAME="mqtt_user"
ENV MQTT_PASSWORD="mqtt_pass"
ENV CHECK_INTERVAL="5"

# Run the application
CMD ["python", "app.py"]
