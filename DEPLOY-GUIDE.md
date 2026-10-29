# TubeFetch ko Live Karne ki Guide (Render — Free)

Code poora taiyaar aur test kiya hua hai. Live karne ke liye sirf 2 account chahiye:
**GitHub** (code rakhne ke liye) aur **Render** (website chalane ke liye) — dono free hain.
Poora kaam lagbhag 15-20 minute ka hai, phone se bhi ho sakta hai, computer se aasan rahega.

## Step 1 — Code GitHub par daalo
1. github.com par account banao / login karo
2. Upar right mein **+ → New repository** → naam do: `tubefetch` → **Create repository**
3. Repo ke page par **uploading an existing file** par click karo
4. Jo ZIP file mili hai (tubefetch-deploy.zip) use pehle kholo/extract karo, phir uske andar ki
   **saari files aur folders** browser mein drag karke upload karo
   (Dhyan: `.venv` folder ZIP mein hai hi nahi — wo chahiye bhi nahi)
5. Neeche **Commit changes** dabao

Files ye honi chahiye repo mein: app.py, requirements.txt, Dockerfile, render.yaml,
templates/index.html, static/style.css, static/app.js, README.md

## Step 2 — Render par live karo
1. render.com par **Get Started** → **GitHub se sign up** karo (wahi GitHub account)
2. Dashboard mein **New → Web Service**
3. Apna `tubefetch` repo chuno (pehli baar Render ko GitHub access dena padega — Allow kar do)
4. Render Dockerfile khud pehchan lega — kuch settings badalne ki zarurat nahi,
   Plan mein **Free** chuno
5. **Create Web Service** dabao — pehli build mein 5-10 minute lagege (ffmpeg + libraries install hongi)
6. Build khatm hote hi upar tumhari live website ka link milega, kuch aisa:
   `https://tubefetch-xxxx.onrender.com`
   Wahi link asli hai — wahi sabko khulega, phone par bhi.

## Live hone ke baad jaan-ne wali baatein
- **Free plan sota hai:** 15 minute koi na aaye to server so jata hai. Agla visitor aane par
  pehla page khulne mein 30-60 second lagte hain — ye free plan ki aadat hai, kharabi nahi.
- **Badi HD files mein time lagega:** Server pehle poori video apne paas download karke merge
  karta hai, phir user ko bhejta hai. 4K / lambi videos mein sabr rakhna — chhoti videos tez hongi.
- **Kabhi YouTube block kare to:** Server ke IP ko YouTube kabhi-kabhi rok deta hai. Aise mein
  aksar yt-dlp update karne se theek hota hai — repo mein requirements.txt ki yt-dlp wali line
  hata kar Render par **Manual Deploy** karne se naya version aa jayega. Muse ko bolna, wo bata dega.
- **Copyright:** Site ko sirf apne khud ke / Creative Commons / permission wale videos ke liye
  promote karna. Isi liye page par ye note pehle se laga hai.

## Muse ko kya chahiye hoga
- Tum bas Step 1 aur Step 2 ke accounts bana lo — koi page atak jaye to screenshot / error
  yahin bhej dena, main bata dunga kya click karna hai.
- Password / OTP Muse ko mat bhejna — login hamesha khud karna.
