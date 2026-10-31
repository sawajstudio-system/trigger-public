import os
import sys
import requests
import datetime

OUTPUT_FILE = "production_report.txt"

# Yahan saari text files ki list hai
TEXT_EXTS = {".py", ".txt", ".yml", ".yaml", ".md", ".json", ".css", ".js", ".sh", ".env", ".sql", ".xml"}
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build"}

files = []
dirs_set = set()

# Dono repos scan karo
for repo in ["Firent", "Backend"]:
    if os.path.isdir(repo):
        for root, dirs, fs in os.walk(repo):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in fs:
                p = os.path.join(root, f)
                if os.path.splitext(p)[1].lower() in TEXT_EXTS:
                    files.append((p, p))
                    # Folder structure nikalne ke liye
                    parts = p.split(os.sep)
                    for i in range(1, len(parts)):
                        dirs_set.add(os.sep.join(parts[:i]))

if not files:
    print("❌ No text files found.")
    sys.exit(1)

# ==========================================
# VIP PREMIUM REPORT GENERATION
# ==========================================
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    # 1. Premium Header
    f.write("╔══════════════════════════════════════════════════════════════════════╗\n")
    f.write("║       👑  VVIP PREMIUM PRODUCTION CODE REPORT  👑                    ║\n")
    f.write("╚══════════════════════════════════════════════════════════════════════╝\n\n")
    
    f.write(f"⏱️  **Generated On:** {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
    f.write(f"📦  **Total Repos:** Firent + Backend\n")
    f.write(f"📄  **Total Files:** {len(files)}\n")
    f.write("━" * 72 + "\n\n")

    # 2. Folder Structure (Tree View)
    f.write("📁 **PROJECT DIRECTORY STRUCTURE**\n")
    f.write("━" * 72 + "\n")
    for d in sorted(dirs_set):
        depth = d.count(os.sep)
        indent = "    " * depth
        folder_name = os.path.basename(d)
        f.write(f"{indent}📂 {folder_name}/\n")
    f.write("\n" + "━" * 72 + "\n\n")

    # 3. Table of Contents
    f.write("📑 **TABLE OF CONTENTS**\n")
    f.write("━" * 72 + "\n")
    for idx, (_, disp) in enumerate(files, 1):
        ext = os.path.splitext(disp)[1].lower()
        icon = "🐍" if ext == ".py" else "📄" if ext in [".txt", ".md"] else "⚙️" if ext in [".yml", ".yaml"] else "📜"
        f.write(f"  {idx:02d}. {icon} {disp}\n")
    f.write("━" * 72 + "\n\n\n")

    # 4. Code Files (VIP Box)
    for idx, (_, p) in enumerate(files, 1):
        try:
            content = open(p, "r", encoding="utf-8", errors="ignore").read()
            
            # File Box Header
            f.write(f"┏{'━' * 70}┓\n")
            f.write(f"┃ 📄 FILE [{idx}/{len(files)}]: {p:<48} ┃\n")
            f.write(f"┗{'━' * 70}┛\n")
            
            # Code block formatting
            f.write("```python\n" if p.endswith('.py') else "```yaml\n" if p.endswith(('.yml', '.yaml')) else "```text\n")
            f.write(content)
            f.write("\n```\n\n\n")
            
        except Exception as e:
            f.write(f"❌ Error reading file {p}: {e}\n\n")

print(f"✅ VVIP Premium Report Generated: {OUTPUT_FILE} ({len(files)} files)")

# ==========================================
# TELEGRAM SEND
# ==========================================
t = os.environ.get("BOT_TOKEN")
c = os.environ.get("CHAT_ID")
if t and c:
    url = f"https://api.telegram.org/bot{t}/sendDocument"
    caption = (
        "👑 <b>VVIP PREMIUM CODE REPORT</b> 👑\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📂 <b>Repos:</b> Firent + Backend\n"
        f"📄 <b>Total Files:</b> {len(files)}\n"
        f"✨ <i>VIP Format & Structure Included</i>"
    )
    try:
        with open(OUTPUT_FILE, "rb") as f:
            requests.post(url, data={"chat_id": c, "caption": caption, "parse_mode": "HTML"}, files={"document": f})
        print("✅ Sent to Telegram!")
    except Exception as e:
        print(f"❌ Telegram Error: {e}")
