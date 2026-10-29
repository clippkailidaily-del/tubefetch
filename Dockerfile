FROM python:3.12-slim

# ffmpeg is required by yt-dlp for merging HD video+audio and for MP3 conversion
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render / Railway / most hosts give the port in $PORT
CMD ["sh", "-c", "gunicorn -w 2 --timeout 600 -b 0.0.0.0:${PORT:-5000} app:app"]
