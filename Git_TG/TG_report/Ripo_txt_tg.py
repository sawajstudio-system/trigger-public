"""
Ripo_txt_tg.py
================
- Firent + Backend dono repos ke saare TEXT files ko ek 'combined_code.txt' mein daalta hai
- Phir Telegram par bhejta hai (TG_sender.py ke through)

Standalone run:
    python Ripo_txt_tg.py
"""

import os
import sys
import traceback

# Isi folder ke TG_sender.py ko import karo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from TG_sender import send_document, build_caption  # noqa: E402

# ============================================================
# CONFIG
# ============================================================
OUTPUT_TXT = "combined_code.txt"
REPOS = ["Firent", "Backend"]

# In folders ki files TXT mein NAHI daalenge
IGNORE_DIRS_IN_TXT = {
    ".git", "node_modules", "venv", ".venv", "__pycache__",
    ".github", "dist", "build", ".next", ".nuxt", ".cache",
    ".pytest_cache", ".mypy_cache", "coverage",
}

# In extensions ko TXT mein skip karenge (binary/known non-code)
IGNORE_EXTS_IN_TXT = {
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
    # Databases / locks / minified
    ".sqlite", ".db", ".lock", ".map",
    ".min.js", ".min.css",
}

# Ye files poora skip karenge
HARD_SKIP_FILES = {".DS_Store", "Thumbs.db", "desktop.ini"}


# ============================================================
# HELPERS
# ============================================================
def log(msg: str) -> None:
    print(msg, flush=True)


def is_text_file(filepath: str) -> bool:
    """
    Binary detection: agar pehle 1024 bytes mein null byte mila to binary hai.
    Text files mein null byte nahi hota.
    """
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(1024)
        return b"\x00" not in chunk
    except Exception:
        return False


def should_skip_in_txt(filename: str, file_path_parts: list) -> bool:
    """TXT mein daalna chahiye ya nahi?"""
    # Extension check
    if any(filename.endswith(ext) for ext in IGNORE_EXTS_IN_TXT):
        return True

    # Directory check
    if any(part in IGNORE_DIRS_IN_TXT for part in file_path_parts):
        return True

    return False


# ============================================================
# BUILDER
# ============================================================
def build_txt() -> tuple:
    """
    combined_code.txt banata hai.
    Returns: (txt_path, file_count, size_mb)
    """
    log("=" * 60)
    log("📂 TXT: Dono repos ka text code combine kiya ja raha hai...")
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
                # Ignore folders ko in-place filter karo (walk efficient rahega)
                dirs[:] = [d for d in dirs if d not in IGNORE_DIRS_IN_TXT]

                for filename in files:
                    if filename in HARD_SKIP_FILES:
                        continue

                    file_path = os.path.join(root, filename)
                    parts = file_path.split(os.sep)

                    # Extension / dir check
                    if should_skip_in_txt(filename, parts):
                        continue

                    # Binary check
                    if not is_text_file(file_path):
                        continue

                    # Read + write
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

    # ---- Stats ----
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

        # ---- Telegram send ----
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
