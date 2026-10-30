# Folder: API
# File: Txt ripo generator.py — FULL FIXED (Both Repos)
import os
import sys
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

SCAN_ROOT = os.environ.get("SCAN_ROOT", ".")
OUTPUT_FILE = os.environ.get("REPORT_FILE", "production_report.txt")
PRIVATE_DIR = "private_source_code"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB per file

SKIP_DIR_NAMES = {
    ".git", "__pycache__", "node_modules", ".venv", "venv",
    "env", "dist", "build", "target", ".next", ".nuxt",
    ".pytest_cache", ".mypy_cache", ".cache", "coverage",
}
SKIP_FILE_NAMES = {OUTPUT_FILE, ".DS_Store", "Thumbs.db", "desktop.ini"}

# ✅ Yahan .yml, .yaml, aur .github folder ki files pakki include hain
TEXT_EXTENSIONS = {
    ".py", ".txt", ".yml", ".yaml", ".md", ".json", ".html",
    ".css", ".js", ".ts", ".sh", ".env", ".sql", ".xml",
    ".toml", ".ini", ".cfg", ".conf", ".dockerfile", ".gitignore"
}


def is_text_file(filepath):
    return os.path.splitext(filepath)[1].lower() in TEXT_EXTENSIONS or filepath.endswith("Dockerfile")


def walk_repo(base_dir, exclude_paths=None):
    exclude_paths = exclude_paths or set()
    for root, dirs, files in os.walk(base_dir, followlinks=False):
        dirs[:] = [
            d for d in dirs
            if d not in SKIP_DIR_NAMES
            and os.path.normpath(os.path.join(root, d)) not in exclude_paths
        ]
        for fname in files:
            if fname in SKIP_FILE_NAMES:
                continue
            fpath = os.path.join(root, fname)
            if os.path.normpath(fpath) in exclude_paths:
                continue
            yield root, fpath


def get_files(base_dir, exclude_paths=None):
    files, seen = [], set()
    for root, fpath in walk_repo(base_dir, exclude_paths):
        norm = os.path.normpath(fpath)
        if norm in seen:
            continue
        if not is_text_file(fpath):
            continue
        seen.add(norm)
        display = norm[2:] if norm.startswith("./") else norm
        files.append((norm, display))
    return files


def main():
    print("=" * 60)
    print("  VIP REPORT GENERATOR STARTING...")
    print("=" * 60)
    
    # ✅ Dono Repos ko scan karega
    repos_to_scan = ["Firent", "Backend"]
    all_files = []

    for repo in repos_to_scan:
        if os.path.isdir(repo):
            print(f"📁 Scanning Repo: {repo}")
            # Har repo ke andar ki files nikal rahe hain
            repo_files = get_files(repo, {os.path.normpath(PRIVATE_DIR)})
            all_files.extend(repo_files)
        else:
            print(f"⚠️ Repo nahi mila: {repo} (Skip)")

    if not all_files:
        print("❌ No text files found to bundle.")
        return 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("╔══════════════════════════════════════════════════════════╗\n")
        f.write("║       👑 VIP PRODUCTION CODE REPORT 👑                   ║\n")
        f.write("╚══════════════════════════════════════════════════════════╝\n\n")

        f.write("📊 EXECUTIVE SUMMARY\n")
        f.write("━" * 60 + "\n")
        f.write(f"⏱️  Date/Time   : {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        f.write(f"📂 Total Files : {len(all_files)}\n")
        f.write("🌐 Repos Scanned: Firent + Backend\n")
        f.write("━" * 60 + "\n\n")

        f.write("📑 TABLE OF CONTENTS (INDEX)\n")
        f.write("━" * 60 + "\n")
        for idx, (_full_p, disp_p) in enumerate(all_files, 1):
            f.write(f"  {idx:02d}. {disp_p}\n")
        f.write("━" * 60 + "\n\n\n")

        for full_path, display_path in all_files:
            try:
                if os.path.getsize(full_path) > MAX_FILE_SIZE:
                    f.write(f"\n[SKIPPED — too large: {display_path}]\n\n")
                    continue

                f.write(f"\n{'=' * 60}\n📄 FILE: {display_path}\n{'=' * 60}\n")
                with open(full_path, "r", encoding="utf-8", errors="ignore") as src:
                    lines = src.read().split("\n")
                    for i, line in enumerate(lines, 1):
                        f.write(f"{i:03d} | {line}\n")
                f.write("\n\n")
            except Exception as e:
                print(f"⚠️  Error reading {display_path}: {e}")
                f.write(f"[Error reading file: {e}]\n\n")

    size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"\n✅ VIP Report generated: {OUTPUT_FILE} ({size_mb:.2f} MB, {len(all_files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
