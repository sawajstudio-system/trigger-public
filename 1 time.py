import os
import glob

print("🚀 Starting One-Time Auto Fixer...")

# 1. Delete Duplicates & Unwanted Files
files_to_delete = [
    "Firent/service_api/utils/Txt ripo generator.py",
    "Firent/service_api/utils/github_03_token_test.py",
    "Firent/.github/workflows/One-Time File.yml",
    "Firent/.github/workflows/One-Time.yml",
    "Firent/.github/workflows/final_fix.yml",
    "Firent/.github/workflows/one_time_fix.yml",
    "Firent/.github/workflows/fix_number.yml",
    "Firent/.github/workflows/run_0_py.yml",
    "0.py",
    "1.py"
]

for f in files_to_delete:
    try:
        if os.path.exists(f):
            os.remove(f)
            print(f"🗑️ Deleted: {f}")
    except Exception as e:
        print(f"❌ Error deleting {f}: {e}")

# 2. Create New VIP Report Generator (Single Source of Truth)
vip_path = "Firent/system_service/TG_report/Ripo_txt_tg.py"
os.makedirs(os.path.dirname(vip_path), exist_ok=True)
vip_code = '''import os, sys, datetime, requests

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
    f.write("╔══════════════════════════════════════════════════════════╗\\n")
    f.write("║       👑 VIP PRODUCTION CODE REPORT 👑                   ║\\n")
    f.write("╚══════════════════════════════════════════════════════════╝\\n\\n")
    f.write(f"Total Files: {len(files)}\\n\\n")
    for _, p in files:
        try:
            f.write(f"\\n{'='*60}\\n📄 FILE: {p}\\n{'='*60}\\n")
            f.write(open(p, "r", encoding="utf-8", errors="ignore").read())
        except: pass

t = os.environ.get("BOT_TOKEN")
c = os.environ.get("CHAT_ID")
if t and c:
    requests.post(f"https://api.telegram.org/bot{t}/sendDocument", data={"chat_id": c, "caption": "VIP Report"}, files={"document": open(OUTPUT_FILE, "rb")})
'''
with open(vip_path, "w", encoding="utf-8") as f:
    f.write(vip_code)
print(f"✅ Created VIP Generator at: {vip_path}")

# 3. Update universal_master.yml Path
yml_file = glob.glob("Firent/.github/workflows/*universal_master*.yml")
if yml_file:
    y = yml_file[0]
    with open(y, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace('FILE="Firent/Ripo_txt_tg.py"', 'FILE="Firent/system_service/TG_report/Ripo_txt_tg.py"')
    with open(y, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Updated path in: {y}")

print("🎉 All fixes applied successfully!")
