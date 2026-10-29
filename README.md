# TubeFetch — YouTube Video Downloader Website

Paste a link → see the video's info and thumbnail → choose a quality (144p up to 4K, whatever is available, or MP3) → download.

## Run it on your own computer

```bash
cd youtube-downloader
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open in your browser: http://localhost:5000

Required: **ffmpeg** must be installed on the system (for merging HD video + audio and for MP3 conversion).
Ubuntu/Debian: `sudo apt install ffmpeg` — Mac: `brew install ffmpeg`

## Put it live on the internet (hosting)

This is a Python (Flask) app, so it cannot run on static hosting like GitHub Pages / Netlify. Options:
- **Render / Railway / PythonAnywhere** — push the repo, start command: `python app.py` (it uses the PORT env var automatically), or deploy with the included Dockerfile
- **Your own VPS** — with gunicorn: `gunicorn -w 2 -b 0.0.0.0:5000 app:app`

Hosting disks are temporary — each downloaded file is deleted from the server right after it is sent to the user (that is how app.py is set up).

## Files
- `app.py` — backend (info + download APIs; only youtube.com / youtu.be links are allowed)
- `templates/index.html` — the page
- `static/style.css`, `static/app.js` — design + frontend logic

## Please note
- Only download videos that you own, that are Creative Commons, or that you have permission for. Re-uploading or selling other people's copyrighted videos is not allowed.
- YouTube occasionally blocks extractors; when that happens, updating yt-dlp (`pip install -U yt-dlp`) usually fixes it.
