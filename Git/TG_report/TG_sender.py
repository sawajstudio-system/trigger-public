"""
TG_sender.py
==============
Sirf Telegram API se baat karne wala helper module.
"""

import os
import requests
from typing import Optional

MAX_TELEGRAM_SIZE_MB = 49.0


def log(msg: str) -> None:
    print(msg, flush=True)


def build_caption(title: str, file_count: int, size_mb: float) -> str:
    actor = os.environ.get("GITHUB_ACTOR", "unknown")
    return (
        f"{title}\n"
        f"📄 {file_count} files | {size_mb:.2f} MB\n"
        f"👤 Manual run: {actor}"
    )


def send_message(
    token: Optional[str],
    chat_id: Optional[str],
    text: str,
    timeout: int = 30,
) -> bool:
    """
    Simple text message Telegram par bhejta hai (sendMessage API).
    ZIP fail/empty hone par notification ke liye useful.
    """
    if not token:
        log("❌ ERROR: BOT_TOKEN missing hai.")
        return False
    if not chat_id:
        log("❌ ERROR: CHAT_ID missing hai.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    log(f"📤 Bhej rahe: text message")

    try:
        response = requests.post(
            url,
            data={"chat_id": chat_id, "text": text},
            timeout=timeout,
        )

        if response.status_code == 200:
            log("   ✅ Sent: text message")
            return True

        try:
            err = response.json().get("description", response.text)
        except Exception:
            err = response.text

        log(f"   ❌ FAILED text: HTTP {response.status_code} — {err}")
        return False

    except requests.exceptions.Timeout:
        log(f"   ❌ TIMEOUT text: {timeout}s se zyada.")
        return False
    except requests.exceptions.RequestException as e:
        log(f"   ❌ NETWORK ERROR text: {e}")
        return False
    except Exception as e:
        log(f"   ❌ UNKNOWN ERROR text: {e}")
        return False


def send_document(
    token: Optional[str],
    chat_id: Optional[str],
    filepath: str,
    caption: str,
    timeout: int = 300,
) -> bool:
    """Ek file Telegram par bhejta hai (sendDocument API)."""
    if not token:
        log("❌ ERROR: BOT_TOKEN missing hai.")
        return False
    if not chat_id:
        log("❌ ERROR: CHAT_ID missing hai.")
        return False
    if not os.path.exists(filepath):
        log(f"❌ ERROR: File nahi mili: {filepath}")
        return False

    size_bytes = os.path.getsize(filepath)
    size_mb = size_bytes / (1024 * 1024)

    if size_mb > MAX_TELEGRAM_SIZE_MB:
        log(f"⚠️  SKIP: {os.path.basename(filepath)} ({size_mb:.2f} MB) > limit")
        return False

    if size_bytes == 0:
        log(f"⚠️  SKIP: {filepath} empty hai.")
        return False

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

        try:
            err = response.json().get("description", response.text)
        except Exception:
            err = response.text

        log(f"   ❌ FAILED {filename}: HTTP {response.status_code} — {err}")
        return False

    except requests.exceptions.Timeout:
        log(f"   ❌ TIMEOUT {filename}: {timeout}s se zyada.")
        return False
    except requests.exceptions.RequestException as e:
        log(f"   ❌ NETWORK ERROR {filename}: {e}")
        return False
    except Exception as e:
        log(f"   ❌ UNKNOWN ERROR {filename}: {e}")
        return False
