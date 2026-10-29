"""
TubeFetch - YouTube Video Downloader Website
Backend: Flask + yt-dlp + ffmpeg

Run:
    pip install -r requirements.txt
    python app.py
Then open http://localhost:5000

Note: Only download videos that you own, or that are Creative Commons /
public domain, or that you otherwise have permission to download.
"""

import os
import re
import shutil
import uuid
from urllib.parse import urlparse

from flask import Flask, after_this_request, jsonify, render_template, request, send_file

try:
    import yt_dlp
except ImportError:  # pragma: no cover
    yt_dlp = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

ALLOWED_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "music.youtube.com",
    "youtu.be",
    "www.youtu.be",
}

app = Flask(__name__)


def is_youtube_url(url: str) -> bool:
    try:
        host = (urlparse(url).hostname or "").lower()
    except Exception:
        return False
    return host in ALLOWED_HOSTS


def clean_url(url: str) -> str:
    """Keep only the video id part of common share URLs (drop tracking params except v/list-safe basics)."""
    url = (url or "").strip()
    return url


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/info")
def video_info():
    if yt_dlp is None:
        return jsonify({"error": "yt-dlp is not installed on the server. Install the packages in requirements.txt."}), 500

    data = request.get_json(force=True, silent=True) or {}
    url = clean_url(data.get("url", ""))

    if not url or not is_youtube_url(url):
        return jsonify({"error": "Please enter a valid YouTube link (youtube.com or youtu.be)."}), 400

    ydl_opts = {"quiet": True, "no_warnings": True, "noplaylist": True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as exc:
        return jsonify({"error": f"Could not fetch video info: {exc}"}), 422

    heights = sorted(
        {
            f["height"]
            for f in info.get("formats", [])
            if f.get("height") and f.get("vcodec") not in (None, "none")
        },
        reverse=True,
    )
    qualities = [h for h in heights if h <= 2160]

    return jsonify(
        {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "uploader": info.get("uploader"),
            "duration": info.get("duration_string"),
            "views": info.get("view_count"),
            "qualities": qualities,
        }
    )


@app.post("/api/download")
def download():
    if yt_dlp is None:
        return jsonify({"error": "yt-dlp is not installed on the server. Install the packages in requirements.txt."}), 500

    data = request.get_json(force=True, silent=True) or {}
    url = clean_url(data.get("url", ""))
    quality = str(data.get("quality", "720"))

    if not url or not is_youtube_url(url):
        return jsonify({"error": "Please enter a valid YouTube link (youtube.com or youtu.be)."}), 400

    job_id = uuid.uuid4().hex[:12]
    job_dir = os.path.join(DOWNLOAD_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    if quality == "audio":
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "format": "bestaudio/best",
            "outtmpl": os.path.join(job_dir, "%(title).80s.%(ext)s"),
            "postprocessors": [
                {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
            ],
        }
    else:
        try:
            height = int(quality)
        except ValueError:
            height = 720
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "format": f"bestvideo[height<={height}]+bestaudio/best[height<={height}]/best",
            "merge_output_format": "mp4",
            "outtmpl": os.path.join(job_dir, "%(title).80s.%(ext)s"),
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as exc:
        shutil.rmtree(job_dir, ignore_errors=True)
        return jsonify({"error": f"Download failed: {exc}"}), 422

    files = [os.path.join(job_dir, f) for f in os.listdir(job_dir) if not f.endswith(".part")]
    if not files:
        shutil.rmtree(job_dir, ignore_errors=True)
        return jsonify({"error": "Download failed: no file was produced."}), 422

    file_path = max(files, key=os.path.getsize)
    download_name = re.sub(r'[\\/:*?"<>|]', "_", os.path.basename(file_path))

    @after_this_request
    def cleanup(response):
        shutil.rmtree(job_dir, ignore_errors=True)
        return response

    return send_file(file_path, as_attachment=True, download_name=download_name)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
