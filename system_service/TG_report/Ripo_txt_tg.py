import os
import sys
import requests
import datetime

# Final Master TXT File
OUTPUT_FILE = "Master_International_Code_Report.txt"

# Har tarah ki text aur code files
TEXT_EXTS = {".py", ".txt", ".yml", ".yaml", ".md", ".json", ".css", ".js", ".ts", ".sh", ".env", ".sql", ".xml", ".toml", ".ini", ".cfg"}
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build", ".pytest_cache", ".mypy_cache"}

all_files = []

# Dono repos ko scan kar raha hai (Firent + Backend)
for repo in ["Firent", "Backend"]:
    if os.path.isdir(repo):
        for root, dirs, fs in os.walk(repo):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in fs:
                p = os.path.join(root, f)
                if os.path.splitext(p)[1].lower() in TEXT_EXTS: 
                    all_files.append(p)

if not all_files:
    print("❌ No code files found.")
    sys.exit(1)

# Sort karo taaki ek order mein aayein
all_files.sort()
total_files = len(all_files)

print(f"📦 Combining {total_files} files into one International Master TXT...")

# ==========================================
# VVIP INTERNATIONAL REPORT GENERATION
# ==========================================
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    # 1. Top Cover (Premium Style)
    f.write("╔══════════════════════════════════════════════════════════════════════╗\n")
    f.write("║  🌍 INTERNATIONAL DEVELOPER MASTER CODE REPORT                       ║\n")
    f.write("║  ──────────────────────────────────────────────────────────────────  ║\n")
    f.write("║  Project: Firent + Backend Ecosystem                                 ║\n")
    f.write("║  Date: " + datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC') + "                               ║\n")
    f.write(f"║  Total Files Included: {total_files:<46} ║\n")
    f.write("║  Status: PRODUCTION READY ✅                                         ║\n")
    f.write("╚══════════════════════════════════════════════════════════════════════╝\n\n\n")

    # 2. Files List & Code Generation
    for idx, p in enumerate(all_files, 1):
        try:
            # File details nikalna
            file_size = os.path.getsize(p) / 1024  # KB
            content = open(p, "r", encoding="utf-8", errors="ignore").read()
            line_count = len(content.split('\n'))
            ext = os.path.splitext(p)[1].lower().replace('.', '')
            
            # Language set karna syntax highlight ke liye
            lang_map = {
                "py": "python", "yml": "yaml", "yaml": "yaml", "js": "javascript",
                "ts": "typescript", "json": "json", "md": "markdown", "sh": "bash",
                "sql": "sql", "xml": "xml", "html": "html", "css": "css"
            }
            lang = lang_map.get(ext, "text")

            # Emoji select karna
            if ext == "py": emoji = "🐍"
            elif ext in ["yml", "yaml"]: emoji = "⚙️"
            elif ext == "md": emoji = "📘"
            elif ext == "json": emoji = "🔧"
            elif ext in ["sh", "env"]: emoji = "💻"
            elif ext in ["js", "ts"]: emoji = "🟨"
            else: emoji = "📄"

            # 🔥 FILE BLOCK HEADER (International Style) 🔥
            f.write("═" * 72 + "\n")
            f.write(f"  📌 FILE [{idx:02d}/{total_files:02d}] : {emoji} {p}\n")
            f.write(f"  ⚖️  Size: {file_size:.2f} KB  |  📝 Lines: {line_count}\n")
            f.write("═" * 72 + "\n\n")
            
            # Code Block (Syntax Highlighting)
            f.write(f"```{lang}\n")
            f.write(content)
            if not content.endswith("\n"):
                f.write("\n")
            f.write("```\n\n\n")  # Extra spaces for separation
            
        except Exception as e:
            f.write(f"❌ Error reading file {p}: {e}\n\n")

print(f"✅ Master Report Generated: {OUTPUT_FILE}")

# ==========================================
# TELEGRAM SEND
# ==========================================
t = os.environ.get("BOT_TOKEN")
c = os.environ.get("CHAT_ID")
if t and c:
    url = f"https://api.telegram.org/bot{t}/sendDocument"
    caption = (
        "🌍 <b>INTERNATIONAL MASTER CODE REPORT</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📂 <b>Repos:</b> Firent + Backend\n"
        f"📄 <b>Total Files:</b> {total_files}\n"
        f"✨ <i>All code combined with International Formatting</i>"
    )
    try:
        with open(OUTPUT_FILE, "rb") as f:
            requests.post(url, data={"chat_id": c, "caption": caption, "parse_mode": "HTML"}, files={"document": f})
        print("✅ Sent to Telegram!")
    except Exception as e:
        print(f"❌ Telegram Error: {e}")
