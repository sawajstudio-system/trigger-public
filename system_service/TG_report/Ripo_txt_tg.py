import os
import sys
import requests
import datetime

OUTPUT_FILE = "production_report.txt"

# ✅ Yahan maine .yml aur .yaml add kar diya hai
TEXT_EXTS = {
    ".py", ".txt", ".yml", ".yaml", ".md", ".json", ".css", ".js", ".sh", 
    ".env", ".sql", ".xml", ".toml", ".ini", ".cfg", ".conf"
}

# ✅ Skip karne wale folders
SKIP_DIRS = {
    ".git", "__pycache__", "node_modules", ".venv", "venv", 
    "dist", "build", ".pytest_cache", ".mypy_cache", ".cache"
}

files = []

# Dono repos scan karega
for repo in ["Firent", "Backend"]:
    if os.path.isdir(repo):
        for root, dirs, fs in os.walk(repo):
            # Skip folders ko hatao
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in fs:
                p = os.path.join(root, f)
                if os.path.splitext(p)[1].lower() in TEXT_EXTS:
                    files.append((p, p))

if not files:
    print("❌ No text files found.")
    sys.exit(1)

# VIP Report Generate karna
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("╔══════════════════════════════════════════════════════════╗\n")
    f.write("║       👑 VIP PRODUCTION CODE REPORT 👑                   ║\n")
    f.write("╚══════════════════════════════════════════════════════════╝\n\n")
    f.write(f"⏱️ Date/Time : {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
    f.write(f"📂 Total Files : {len(files)}\n")
    f.write("🌐 Repos: Firent + Backend\n")
    f.write("━" * 60 + "\n\n📑 INDEX\n" + "━" * 60 + "\n")

    for idx, (_, disp) in enumerate(files, 1):
        f.write(f"{idx:02d}. {disp}\n")
    f.write("━" * 60 + "\n\n")

    for _, p in files:
        try:
            f.write(f"\n{'='*60}\n📄 FILE: {p}\n{'='*60}\n")
            f.write(open(p, "r", encoding="utf-8", errors="ignore").read())
        except Exception as e:
            f.write(f"[Error reading file: {e}]\n")

print(f"✅ Generated: {OUTPUT_FILE} ({len(files)} files)")

# Telegram par bhejna
t = os.environ.get("BOT_TOKEN")
c = os.environ.get("CHAT_ID")
if t and c:
    url = f"https://api.telegram.org/bot{t}/sendDocument"
    try:
        with open(OUTPUT_FILE, "rb") as f:
            requests.post(url, data={"chat_id": c, "caption": f"👑 VIP Report ({len(files)} files)"}, files={"document": f})
        print("✅ Sent to Telegram!")
    except Exception as e:
        print(f"❌ Telegram Error: {e}")
