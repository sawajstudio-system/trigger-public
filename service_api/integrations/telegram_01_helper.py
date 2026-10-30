# =============================================================================
#  TELEGRAM HELPER — Centralized message delivery
# =============================================================================
#  Purpose : Single source of truth for sending Telegram messages from any
#            script in this project. Handles env var validation, timeouts,
#            error logging, and safe printing (never logs tokens).
#
#  Author  : Sawaj Studio System
#  Version : 2.0.0
# =============================================================================

from __future__ import annotations

import logging
import os
from typing import Optional

import requests


# =============================================================================
#  LOGGER
# =============================================================================
#  Use logging (not print) so output is timestamped and can be filtered.
#  Level controlled by LOG_LEVEL env var (default: INFO).
# =============================================================================
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
)
logger = logging.getLogger("telegram_helper")


# =============================================================================
#  CONFIGURATION
# =============================================================================
TELEGRAM_API_BASE = "https://api.telegram.org"
REQUEST_TIMEOUT_SECONDS = 15


# =============================================================================
#  PUBLIC API
# =============================================================================
def send_telegram_message(message_text: str) -> bool:
    """
    Send a plain-text message to the configured Telegram chat.

    Args:
        message_text: The message body (plain text, max 4096 chars).

    Returns:
        True if the message was delivered successfully, False otherwise.

    Raises:
        Nothing — all errors are logged and swallowed. Callers should not
        crash because of a Telegram failure.

    Environment variables required:
        TELEGRAM_API_REPORT_TOKEN   — Bot API token (secret)
        TELEGRAM_API_REPORT_CHAT_ID — Target chat ID (e.g., "-1001234567890")
    """
    # -------------------------------------------------------------------------
    # Validate inputs
    # -------------------------------------------------------------------------
    if not message_text or not message_text.strip():
        logger.warning("Refusing to send empty message.")
        return False

    if len(message_text) > 4096:
        logger.warning(
            "Message truncated from %d to 4096 chars (Telegram limit).",
            len(message_text),
        )
        message_text = message_text[:4093] + "..."

    token: Optional[str] = os.getenv("TELEGRAM_API_REPORT_TOKEN")
    chat_id: Optional[str] = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")

    if not token or not chat_id:
        logger.error(
            "Telegram credentials missing. "
            "Set TELEGRAM_API_REPORT_TOKEN and TELEGRAM_API_REPORT_CHAT_ID."
        )
        return False

    # -------------------------------------------------------------------------
    # Send request
    # -------------------------------------------------------------------------
    # NOTE: URL contains the token. Do NOT log `url` directly — that would
    # leak the secret into CI logs. GitHub masks known secrets, but defense
    # in depth: we simply never log it.
    url = f"{TELEGRAM_API_BASE}/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message_text, "parse_mode": "HTML"}

    try:
        response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT_SECONDS)
    except requests.Timeout:
        logger.error("Telegram request timed out after %ss.", REQUEST_TIMEOUT_SECONDS)
        return False
    except requests.RequestException as exc:
        # Redact the token from the exception message before logging.
        logger.error("Telegram request failed: %s", _redact(str(exc), token))
        return False

    # -------------------------------------------------------------------------
    # Interpret response
    # -------------------------------------------------------------------------
    if response.status_code == 200:
        logger.info("Telegram message delivered successfully.")
        return True

    # Log status + redacted response body (never the raw URL).
    body = _redact(response.text or "", token)
    logger.error(
        "Telegram API returned HTTP %s: %s",
        response.status_code,
        body[:500],  # cap log size
    )
    return False


# =============================================================================
#  INTERNAL HELPERS
# =============================================================================
def _redact(text: str, secret: str) -> str:
    """Replace the secret token with a placeholder in any string."""
    if not secret:
        return text
    return text.replace(secret, "<REDACTED_TOKEN>")


# =============================================================================
#  SELF-TEST (run: python telegram_01_helper.py)
# =============================================================================
if __name__ == "__main__":
    ok = send_telegram_message(
        "🔧 <b>Helper self-test</b>\nTelegram helper is working correctly."
    )
    raise SystemExit(0 if ok else 1)
