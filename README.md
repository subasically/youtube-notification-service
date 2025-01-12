# YouTube Notification Service

This project is a YouTube notification service that monitors a specified YouTube channel for new video uploads and sends notifications via a webhook.

## Features

- Monitors a YouTube channel for new video uploads.
- Sends notifications via a webhook when a new video is detected.
- Maintains a history of notifications to avoid duplicate alerts.
- Configurable check interval and video title pattern matching.

## Prerequisites

- Docker
- Docker Compose

## Environment Variables

- `YOUTUBE_CHANNEL_ID`: The ID of the YouTube channel to monitor.
- `WEBHOOK_URL`: The URL of the webhook to send notifications to.
- `CHECK_INTERVAL`: The interval (in minutes) at which to check for new videos. Default is 5 minutes.
- `VIDEO_TITLE`: The default title pattern to match for new videos.

## Setup

1. Clone the repository:

```sh
git clone https://github.com/yourusername/youtube-notification-service.git
cd youtube-notification-service
```

2. Create a `.env` file in the root directory and add the required environment variables:

```env
YOUTUBE_CHANNEL_ID=your_channel_id
WEBHOOK_URL=your_webhook_url
CHECK_INTERVAL=15
VIDEO_TITLE="Your Video Title"
```

3. Build and run the service using Docker Compose:

```sh
docker-compose up --build
```

## Files

- `app.py`: Main application script that monitors the YouTube channel and sends notifications.
- `match.py`: Contains the logic for matching video titles.
- `logger.py`: Configures the logging for the application.
- `notification-history.json`: Stores the history of notifications to avoid duplicates.
- `Dockerfile`: Dockerfile to build the application image.
- `docker-compose.yml`: Docker Compose configuration file.

## Usage

The service will start monitoring the specified YouTube channel and send notifications to the configured webhook URL. Logs will be output to the console.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Contact

For any questions or issues, please open an issue on the GitHub repository.
