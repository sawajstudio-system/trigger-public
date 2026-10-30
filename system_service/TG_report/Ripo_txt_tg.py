"""
Ripo_txt_tg.py
================
- Dono repos ki saari TEXT files → combined_code.txt
- ZIP wali files yahan NAHI aayengi (complementary)
- Telegram par bhejta hai

Standalone run:
    python Ripo_txt_tg.py
"""

import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from TG_sender import send_document, build_caption  # noqa: E402

# ============================================================
# CONFIG — ZIP wale se EXACT match karna chahiye
# ============================================================
OUTPUT_TXT = "combined_code.txt"
REPOS = ["Firent", "Backend"]

HARD_SKIP_DIRS = {
    ".git", "node_modules", "venv", ".venv", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".cache", "coverage",
    "dist", "build", ".next", ".nuxt",
}

HARD_SKIP_FILES = {".DS_Store", "Thumbs.db", "desktop.ini"}

NON_TEXT_EXTS = {
    # Images
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".webp", ".bmp", ".tiff",
    # Archives
    ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz",
    # Documents
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    # Binaries
    ".exe", ".dll", ".so", ".dylib", ".bin", ".o", ".a", ".pyc", ".pyo",
    # Media
    ".mp4", ".mp3", ".wav", ".avi", ".mov", ".mkv", ".flv", ".webm",
    # Fonts
    ".ttf", ".otf", ".woff", ".woff2", ".eot",
    # Databases / locks
    ".sqlite", ".db", ".lock", ".map",
    ".min.js", ".min.css",
}


# ============================================================
# HELPERS
# ============================================================
def log(msg: str) -> None:
    print(msg, flush=True)


def is_text_file(filepath: str) -> bool:
    """Null byte check — text files mein null byte nahi hota."""
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(1024)
        return b"\x00" not in chunk
    except Exception:
        return False


def classify(file_path: str) -> str:
    """
    File ko classify karta hai:
      "skip" → dono se bahar
      "zip"  → ZIP mein
      "txt"  → TXT mein
    """
    filename = os.path.basename(file_path)
    parts = file_path.split(os.sep)

    if filename in HARD_SKIP_FILES:
        return "skip"
    if any(part in HARD_SKIP_DIRS for part in parts):
        return "skip"
    if any(filename.endswith(ext) for ext in NON_TEXT_EXTS):
        return "zip"
    if not is_text_file(file_path):
        return "zip"
    return "txt"


# ============================================================
# BUILDER
# ============================================================
def build_txt() -> tuple:
    log("=" * 60)
    log("📂 TXT: Text files combine ki ja rahi hain...")
    log("=" * 60)

    file_count = 0

    with open(OUTPUT_TXT, "w", encoding="utf-8", errors="ignore") as outfile:
        outfile.write("=== FIRENT & BACKEND BOTH REPOSITORIES CODE ===\n")
        outfile.write(f"Generated: {os.popen('date -u').read().strip()}\n")
        outfile.write(f"Repos: {', '.join(REPOS)}\n\n")

        for repo in REPOS:
            if not os.path.exists(repo):
                log(f"⚠️  Folder nahi mila: {repo} — skip")
                continue

            log(f"\n▶ Processing: {repo}")
            repo_count = 0

            for root, dirs, files in os.walk(repo):
                dirs[:] = [d for d in dirs if d not in HARD_SKIP_DIRS]

                for filename in files:
                    file_path = os.path.join(root, filename)

                    if classify(file_path) != "txt":
                        continue

                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
                            content = infile.read()

                        outfile.write("\n\n" + "=" * 70 + "\n")
                        outfile.write(f"FILE: {file_path}\n")
                        outfile.write("=" * 70 + "\n\n")
                        outfile.write(content)

                        file_count += 1
                        repo_count += 1
                    except Exception as e:
                        log(f"   ⚠️  Read error: {file_path} → {e}")

            log(f"   ✅ {repo} — {repo_count} files collected")

    size_mb = os.path.getsize(OUTPUT_TXT) / (1024 * 1024) if os.path.exists(OUTPUT_TXT) else 0.0

    log("\n" + "=" * 60)
    log(f"📊 TXT: Total {file_count} files | {size_mb:.2f} MB")
    log("=" * 60)

    return OUTPUT_TXT, file_count, size_mb


# ============================================================
# MAIN
# ============================================================
def main() -> int:
    try:
        txt_path, count, size_mb = build_txt()

        if count == 0:
            log("❌ ERROR: Koi text file nahi mili. Abort.")
            return 1

        log("\n📤 Telegram par TXT bheja ja raha hai...")
        caption = build_caption("📄 Firent & Backend Code (TXT)", count, size_mb)

        ok = send_document(
            token=os.environ.get("BOT_TOKEN"),
            chat_id=os.environ.get("CHAT_ID"),
            filepath=txt_path,
            caption=caption,
        )

        if not ok:
            log("❌ TXT send fail ho gaya.")
            return 1

        log("\n✅ TXT: Done!")
        return 0

    except Exception as e:
        log(f"❌ FATAL ERROR: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
