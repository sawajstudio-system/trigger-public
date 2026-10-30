"""
TG_sender.py
================
Sirf Telegram API se baat karne wala helper module.

Koi file processing NAHI — sirf ek file bhejna.
Dono scripts (Ripo_txt_tg.py, Ripo_zip_tg.py) ise import karti hain.

Usage:
    from TG_sender import send_document
    ok = send_document(token, chat_id, filepath, caption)
"""

import os
import requests
from typing import Optional

# Telegram bot ki per-file limit 50 MB hai
MAX_TELEGRAM_SIZE_MB = 49.0


def log(msg: str) -> None:
    """Simple logger (GitHub Actions mein print karta hai)."""
    print(msg, flush=True)


def _human_size(num_bytes: int) -> str:
    """Bytes ko readable format mein badalta hai."""
    for unit in ["B", "KB", "MB", "GB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.2f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.2f} TB"


def send_document(
    token: Optional[str],
    chat_id: Optional[str],
    filepath: str,
    caption: str,
    timeout: int = 300,
) -> bool:
    """
    Ek file Telegram par bhejta hai (sendDocument API).

    Args:
        token: Telegram bot token (BOT_TOKEN env se aayega)
        chat_id: Telegram chat/channel ID (CHAT_ID env se aayega)
        filepath: Local file ka path
        caption: File ke saath message
        timeout: Request timeout (seconds)

    Returns:
        True agar successfully bhej diya, False warna.
    """
    # ---- Validation ----
    if not token:
        log("❌ ERROR: BOT_TOKEN missing hai. Telegram nahi bhej sakte.")
        return False

    if not chat_id:
        log("❌ ERROR: CHAT_ID missing hai. Telegram nahi bhej sakte.")
        return False

    if not os.path.exists(filepath):
        log(f"❌ ERROR: File nahi mili: {filepath}")
        return False

    # ---- Size check ----
    size_bytes = os.path.getsize(filepath)
    size_mb = size_bytes / (1024 * 1024)

    if size_mb > MAX_TELEGRAM_SIZE_MB:
        log(
            f"⚠️  SKIP: {os.path.basename(filepath)} "
            f"({size_mb:.2f} MB) Telegram limit ({MAX_TELEGRAM_SIZE_MB} MB) "
            f"se bada hai."
        )
        return False

    if size_bytes == 0:
        log(f"⚠️  SKIP: {filepath} empty hai (0 bytes).")
        return False

    # ---- Send ----
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    filename = os.path.basename(filepath)
    log(f"📤 Bhej rahe: {filename} ({size_mb:.2f} MB)")

    try:
        with open(filepath, "rb") as f:
            response = requests.post(
                url,
                data={"chat_id": chat_id, "caption": caption},
                files={"document": f},
                timeout=timeout,
            )

        if response.status_code == 200:
            log(f"   ✅ Sent: {filename}")
            return True

        # Telegram error message nikaalne ki koshish
        try:
            err = response.json().get("description", response.text)
        except Exception:
            err = response.text

        log(f"   ❌ FAILED {filename}: HTTP {response.status_code} — {err}")
        return False

    except requests.exceptions.Timeout:
        log(f"   ❌ TIMEOUT {filename}: {timeout}s se zyada lag gaya.")
        return False
    except requests.exceptions.RequestException as e:
        log(f"   ❌ NETWORK ERROR {filename}: {e}")
        return False
    except Exception as e:
        log(f"   ❌ UNKNOWN ERROR {filename}: {e}")
        return False


def build_caption(title: str, file_count: int, size_mb: float) -> str:
    """Standard caption banata hai (consistency ke liye)."""
    actor = os.environ.get("GITHUB_ACTOR", "unknown")
    return (
        f"{title}\n"
        f"📄 {file_count} files | {size_mb:.2f} MB\n"
        f"👤 Manual run: {actor}"
    )
