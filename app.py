from flask import Flask, request, jsonify, abort
import yt_dlp
import os

app = Flask(__name__)

# Simple API key for authentication
API_KEY = "your_secret_api_key_here"

# Folder to save downloaded videos
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_video(url):
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
    return info['title'], ydl_opts['outtmpl'] % info

@app.before_request
def check_auth():
    token = request.headers.get('X-API-KEY')
    if token != API_KEY:
        abort(401, description="Unauthorized: Invalid API Key")

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        title, filepath = download_video(url)
        return jsonify({
            "message": f"Video '{title}' downloaded successfully",
            "file_path": filepath
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "<h3>YouTube Downloader API is running</h3>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
