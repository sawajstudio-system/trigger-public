"""
Ripo_zip_tg.py
================
- Firent + Backend dono repos ki SAARI non-text files
  (images, PDFs, ZIPs, exe, videos, etc.) ko 'ignored_files.zip' mein pack karta hai
- Phir Telegram par bhejta hai (TG_sender.py ke through)

Standalone run:
    python Ripo_zip_tg.py
"""

import os
import sys
import zipfile
import traceback

# Isi folder ke TG_sender.py ko import karo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from TG_sender import send_document, build_caption  # noqa: E402

# ============================================================
# CONFIG
# ============================================================
OUTPUT_ZIP = "ignored_files.zip"
REPOS = ["Firent", "Backend"]

# Ye folders poora skip — ZIP mein bhi nahi dalenge (bahut heavy)
HARD_SKIP_DIRS = {
    ".git", "node_modules", "venv", ".venv", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".cache", "coverage",
}

# Ye files poora skip
HARD_SKIP_FILES = {".DS_Store", "Thumbs.db", "desktop.ini"}

# In extensions ko ZIP mein DAALENGE (jo TXT mein nahi gayi)
INCLUDE_EXTS_IN_ZIP = {
    # Images
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".webp", ".bmp", ".tiff",
    # Archives
    ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz",
    # Documents
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    # Binaries
    ".exe", ".dll", ".so", ".dylib", ".bin", ".o", ".a",
    # Media
    ".mp4", ".mp3", ".wav", ".avi", ".mov", ".mkv", ".flv", ".webm",
    # Fonts
    ".ttf", ".otf", ".woff", ".woff2", ".eot",
    # Databases
    ".sqlite", ".db",
}


# ============================================================
# HELPERS
# ============================================================
def log(msg: str) -> None:
    print(msg, flush=True)


def should_include_in_zip(filename: str, file_path_parts: list) -> bool:
    """Kya yeh file ZIP mein daalni chahiye?"""
    if filename in HARD_SKIP_FILES:
        return False

    if any(part in HARD_SKIP_DIRS for part in file_path_parts):
        return False

    # Sirf known non-text extensions hi include karo
    return any(filename.endswith(ext) for ext in INCLUDE_EXTS_IN_ZIP)


# ============================================================
# BUILDER
# ============================================================
def build_zip() -> tuple:
    """
    ignored_files.zip banata hai.
    Returns: (zip_path, file_count, size_mb)
    """
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
                # Hard skip dirs ko filter karo
                dirs[:] = [d for d in dirs if d not in HARD_SKIP_DIRS]

                for filename in files:
                    file_path = os.path.join(root, filename)
                    parts = file_path.split(os.sep)

                    if not should_include_in_zip(filename, parts):
                        continue

                    try:
                        # arcname mein repo prefix rakho taaki dono repos ka
                        # structure clear rahe zip ke andar
                        zipf.write(file_path, arcname=file_path)
                        file_count += 1
                        repo_count += 1
                    except Exception as e:
                        log(f"   ⚠️  ZIP error: {file_path} → {e}")

            log(f"   ✅ {repo} — {repo_count} files packed")

    # ---- Stats ----
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
            return 0  # Fail nahi — TXT already chali gayi hogi

        # ---- Telegram send ----
        log("\n📤 Telegram par ZIP bheja ja raha hai...")
        caption = build_caption("🗜️  Ignored Files (ZIP)", count, size_mb)

        ok = send_document(
            token=os.environ.get("BOT_TOKEN"),
            chat_id=os.environ.get("CHAT_ID"),
            filepath=zip_path,
            caption=caption,
            timeout=600,  # ZIP bada ho sakta hai
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
