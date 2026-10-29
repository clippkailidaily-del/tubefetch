# TubeFetch — YouTube Video Downloader Website

Link paste karo → video ki info + thumbnail dekho → quality chuno (144p se 4K tak jo available ho, ya MP3) → download.

## Apne computer par chalana

```bash
cd youtube-downloader
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Browser mein kholo: http://localhost:5000

Zaruri: system par **ffmpeg** install hona chahiye (HD video + audio merge aur MP3 ke liye).
Ubuntu/Debian: `sudo apt install ffmpeg` — Mac: `brew install ffmpeg`

## Internet par live karna (hosting)

Ye ek Python (Flask) app hai, isliye GitHub Pages / Netlify jaisi static hosting par nahi chalegi. Options:
- **Render / Railway / PythonAnywhere** — repo push karo, start command: `python app.py` (PORT env ye khud use kar leta hai)
- **Apna VPS** — gunicorn ke saath: `gunicorn -w 2 -b 0.0.0.0:5000 app:app`

Hosting par disk temporary hoti hai — download ki hui file user ko bhejkar server se turant delete ho jati hai (app.py mein yahi setup hai).

## Files
- `app.py` — backend (info + download APIs, sirf youtube.com / youtu.be links allow hain)
- `templates/index.html` — page
- `static/style.css`, `static/app.js` — design + frontend logic

## Dhyan do
- Sirf apne khud ke, Creative Commons, ya permission wale videos download karo. Dusron ke copyright videos ko re-upload / bechna galat hai.
- YouTube kabhi-kabhi apni taraf se extractor block karta hai; tab `pip install -U yt-dlp` se update karna padta hai.
