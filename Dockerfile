# Use Python 3.9 image
FROM python:alpine

# Set working directory
WORKDIR /app

# Install ffmpeg
RUN apk add --no-cache ffmpeg

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Run the application
CMD ["python", "app.py"]
