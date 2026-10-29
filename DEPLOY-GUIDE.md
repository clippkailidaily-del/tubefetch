# How to Put TubeFetch Live (Render — Free)

The code is fully ready and tested. Going live needs only 2 free accounts:
**GitHub** (to hold the code) and **Render** (to run the website).
The whole thing takes about 15-20 minutes.

## Step 1 — Put the code on GitHub
1. Create an account / log in at github.com
2. Top right: **+ → New repository** → name it `tubefetch` → **Create repository**
3. On the repo page, click **uploading an existing file**
4. Extract the ZIP (tubefetch-deploy.zip) first, then upload **all the files and folders** inside it
   (the `.venv` folder is not in the ZIP — it is not needed)
5. Click **Commit changes**

The repo should contain: app.py, requirements.txt, Dockerfile, render.yaml,
templates/index.html, static/style.css, static/app.js, README.md

## Step 2 — Go live on Render
1. Sign up at render.com **with GitHub**
2. In the dashboard: **New → Web Service**
3. Choose your `tubefetch` repo (the first time, Render will ask for GitHub access — allow it)
4. Render detects the Dockerfile automatically — no settings to change. Choose the **Free** plan
5. Click **Create Web Service** — the first build takes 5-10 minutes (ffmpeg and the libraries get installed)
6. When the build finishes, your live website address appears at the top, something like:
   `https://tubefetch-xxxx.onrender.com`
   That is the real link — it opens for everyone, on phones too.

## Good to know after going live
- **The free plan sleeps:** if nobody visits for 15 minutes, the server goes to sleep. The next visitor's first page load takes 30-60 seconds — that is normal free-plan behavior, not a bug.
- **Large HD files take time:** the server first downloads the whole video, merges it, then sends it to the user. Long / 4K videos need patience; short videos are fast.
- **If YouTube blocks it someday:** YouTube sometimes blocks server IPs. Updating yt-dlp usually fixes it — remove/re-add the yt-dlp line in requirements.txt and use **Manual Deploy** on Render to rebuild.
- **Copyright:** Promote the site only for your own / Creative Commons / permitted videos. That is why the note is already on the page.
