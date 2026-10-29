const $ = (id) => document.getElementById(id);

function showError(msg) {
  const el = $("error");
  el.textContent = msg || "";
  el.hidden = !msg;
}

async function fetchInfo() {
  showError("");
  $("status").textContent = "";
  const url = $("url").value.trim();
  if (!url) { showError("Pehle YouTube ka link paste karo."); return; }

  const btn = $("fetchBtn");
  btn.disabled = true; btn.textContent = "Loding...";
  try {
    const res = await fetch("/api/info", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Kuch galat ho gaya.");

    $("thumb").src = data.thumbnail || "";
    $("title").textContent = data.title || "";
    const bits = [];
    if (data.uploader) bits.push(data.uploader);
    if (data.duration) bits.push("⏱ " + data.duration);
    if (data.views) bits.push("👁 " + Number(data.views).toLocaleString("en-IN") + " views");
    $("meta").textContent = bits.join(" • ");

    const sel = $("quality");
    sel.innerHTML = "";
    (data.qualities || [720]).forEach((h) => {
      const opt = document.createElement("option");
      opt.value = h; opt.textContent = h + "p MP4";
      if (h === 720) opt.selected = true;
      sel.appendChild(opt);
    });
    const audio = document.createElement("option");
    audio.value = "audio"; audio.textContent = "MP3 — sirf audio";
    sel.appendChild(audio);

    $("result").hidden = false;
  } catch (e) {
    showError(e.message);
    $("result").hidden = true;
  } finally {
    btn.disabled = false; btn.textContent = "Video Lao";
  }
}

async function startDownload() {
  showError("");
  const url = $("url").value.trim();
  const quality = $("quality").value;
  const btn = $("downloadBtn");
  btn.disabled = true;
  $("status").textContent = "Server video taiyaar kar raha hai... HD quality mein thoda time lag sakta hai, page band mat karna.";
  try {
    const res = await fetch("/api/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, quality }),
    });
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.error || "Download fail ho gaya.");
    }
    const blob = await res.blob();
    const disp = res.headers.get("Content-Disposition") || "";
    const match = disp.match(/filename="?([^"]+)"?/);
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = match ? decodeURIComponent(match[1]) : "video.mp4";
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 4000);
    $("status").textContent = "Download shuru ho gaya ✅ Apne Downloads folder mein check karo.";
  } catch (e) {
    showError(e.message);
    $("status").textContent = "";
  } finally {
    btn.disabled = false;
  }
}

$("url").addEventListener("keydown", (e) => { if (e.key === "Enter") fetchInfo(); });
