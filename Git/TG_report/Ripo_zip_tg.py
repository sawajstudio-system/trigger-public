"""
Ripo_zip_tg.py
================
- Dono repos ki saari NON-TEXT files → ignored_files.zip
- TXT wali files yahan NAHI aayengi (complementary)
- Telegram par bhejta hai

Standalone run:
    python Ripo_zip_tg.py
"""

import os
import sys
import zipfile
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from TG_sender import send_document, build_caption  # noqa: E402

# ============================================================
# CONFIG — TXT wale se EXACT match karna chahiye
# ============================================================
OUTPUT_ZIP = "ignored_files.zip"
REPOS = ["Firent", "Backend"]

HARD_SKIP_DIRS = {
    ".git", "node_modules", "venv", ".venv", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".cache", "coverage",
    "dist", "build", ".next", ".nuxt",
}

HARD_SKIP_FILES = {".DS_Store", "Thumbs.db", "desktop.ini"}

NON_TEXT_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".webp", ".bmp", ".tiff",
    ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".exe", ".dll", ".so", ".dylib", ".bin", ".o", ".a", ".pyc", ".pyo",
    ".mp4", ".mp3", ".wav", ".avi", ".mov", ".mkv", ".flv", ".webm",
    ".ttf", ".otf", ".woff", ".woff2", ".eot",
    ".sqlite", ".db", ".lock", ".map",
    ".min.js", ".min.css",
}


# ============================================================
# HELPERS
# ============================================================
def log(msg: str) -> None:
    print(msg, flush=True)


def is_text_file(filepath: str) -> bool:
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(1024)
        return b"\x00" not in chunk
    except Exception:
        return False


def classify(file_path: str) -> str:
    """TXT wale se EXACT same logic."""
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
def build_zip() -> tuple:
    log("=" * 60)
    log("🗜️  ZIP: Non-text files pack ki ja rahi hain...")
    log("=" * 60)

    file_count = 0

    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zipf:
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

                    if classify(file_path) != "zip":
                        continue

                    try:
                        zipf.write(file_path, arcname=file_path)
                        file_count += 1
                        repo_count += 1
                    except Exception as e:
                        log(f"   ⚠️  ZIP error: {file_path} → {e}")

            log(f"   ✅ {repo} — {repo_count} files packed")

    size_mb = os.path.getsize(OUTPUT_ZIP) / (1024 * 1024) if os.path.exists(OUTPUT_ZIP) else 0.0

    log("\n" + "=" * 60)
    log(f"📊 ZIP: Total {file_count} files | {size_mb:.2f} MB")
    log("=" * 60)

    return OUTPUT_ZIP, file_count, size_mb


# ============================================================
# MAIN
# ============================================================
def main() -> int:
    try:
        zip_path, count, size_mb = build_zip()

        if count == 0:
            log("⚠️  Koi non-text file nahi mili. ZIP nahi bhejenge.")
            return 0

        log("\n📤 Telegram par ZIP bheja ja raha hai...")
        caption = build_caption("🗜️  Ignored Files (ZIP)", count, size_mb)

        ok = send_document(
            token=os.environ.get("BOT_TOKEN"),
            chat_id=os.environ.get("CHAT_ID"),
            filepath=zip_path,
            caption=caption,
            timeout=600,
        )

        if not ok:
            log("❌ ZIP send fail ho gaya.")
            return 1

        log("\n✅ ZIP: Done!")
        return 0

    except Exception as e:
        log(f"❌ FATAL ERROR: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
