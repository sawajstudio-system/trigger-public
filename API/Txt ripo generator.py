# Folder: API
# File: Txt ripo generator.py
import os
import sys
import datetime

OUTPUT_FILE = os.getenv("REPORT_FILE", "production_report.txt")
PRIVATE_DIR = "private_source_code"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB limit per file

SKIP_DIR_NAMES = {".git", "__pycache__", "node_modules", ".venv", "venv", "env", "dist", "build", "target"}
SKIP_FILE_NAMES = {OUTPUT_FILE, ".DS_Store", "Thumbs.db"}
TEXT_EXTENSIONS = {".py", ".txt", ".yml", ".yaml", ".md", ".json", ".html", ".css", ".js", ".ts", ".sh", ".env", ".sql", ".xml"}

def is_text_file(filepath):
    return os.path.splitext(filepath)[1].lower() in TEXT_EXTENSIONS

def walk_repo(base_dir, exclude_paths=None):
    exclude_paths = exclude_paths or set()
    for root, dirs, files in os.walk(base_dir, followlinks=False):
        dirs[:] = [d for d in dirs if d not in SKIP_DIR_NAMES and os.path.normpath(os.path.join(root, d)) not in exclude_paths]
        for fname in files:
            if fname in SKIP_FILE_NAMES: continue
            fpath = os.path.join(root, fname)
            if os.path.normpath(fpath) in exclude_paths: continue
            yield root, fpath

def get_files(base_dir, exclude_paths=None):
    files, seen = [], set()
    for root, fpath in walk_repo(base_dir, exclude_paths):
        norm = os.path.normpath(fpath)
        if norm not in seen and is_text_file(fpath):
            seen.add(norm)
            display = norm[2:] if norm.startswith("./") else norm
            files.append((norm, display))
    return files

def main():
    print("=" * 60)
    print("  VIP REPORT GENERATOR STARTING...")
    print("=" * 60)

    base_scan_dir = "../../" if os.path.basename(os.getcwd()) == "API" else "."
    public_exclude = {os.path.normpath(PRIVATE_DIR)}
    
    public_files = get_files(base_scan_dir, public_exclude)
    private_files = get_files(PRIVATE_DIR) if os.path.isdir(PRIVATE_DIR) else []
    all_files = public_files + private_files

    if not all_files:
        print("No text files found to bundle.")
        return 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("╔══════════════════════════════════════════════════════════╗\n")
        f.write("║       👑 VIP PRODUCTION CODE REPORT 👑                   ║\n")
        f.write("╚══════════════════════════════════════════════════════════╝\n\n")
        
        f.write("📊 EXECUTIVE SUMMARY\n")
        f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        f.write(f"⏱️  Date/Time   : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        f.write(f"📂 Total Files : {len(all_files)}\n")
        f.write(f"🌐 Public Repo : {len(public_files)} files\n")
        f.write(f"🔒 Private Repo: {len(private_files)} files\n")
        f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n")

        f.write("📑 TABLE OF CONTENTS (INDEX)\n")
        f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        for idx, (full_p, disp_p) in enumerate(all_files, 1):
            f.write(f"  {idx:02d}. {disp_p}\n")
        f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n\n")

        for full_path, display_path in all_files:
            try:
                if os.path.getsize(full_path) > MAX_FILE_SIZE:
                    continue
                
                f.write(f"\n{'='*60}\n📄 FILE: {display_path}\n{'='*60}\n")
                with open(full_path, "r", encoding="utf-8", errors="ignore") as src:
                    lines = src.read().split('\n')
                    for i, line in enumerate(lines, 1):
                        f.write(f"{i:03d} | {line}\n")
                f.write("\n\n")
            except Exception as e:
                print(f"Error reading {display_path}: {e}")
                f.write(f"[Error reading file: {e}]\n\n")

    print(f"\n✅ VIP Report generated: {OUTPUT_FILE}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
