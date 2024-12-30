from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "channel_url": CHANNEL_URL,
        "last_video_id": last_video_id,
    })

@app.route('/update_channel/<path:channel_url>', methods=['POST'])
def update_channel(channel_url):
    global CHANNEL_URL, last_video_id
    CHANNEL_URL = channel_url
    last_video_id = None  # Reset to detect all videos as new
    return jsonify({"message": f"Channel updated to {channel_url}"}), 200

if __name__ == "__main__":
    from threading import Thread
    tracker_thread = Thread(target=track_videos)
    tracker_thread.start()
    app.run(host="0.0.0.0", port=5000)
