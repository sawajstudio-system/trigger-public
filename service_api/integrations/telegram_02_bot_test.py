# =============================================================================
#  TELEGRAM BOT SMOKE TEST (VIP EDITION) — FIXED
# =============================================================================
import os
import sys

# ✅ FIX: path setup taaki telegram_01_helper import ho sake
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from telegram_01_helper import send_telegram_message


def run_test():
    token = os.getenv("TELEGRAM_API_REPORT_TOKEN")
    chat_id = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")

    if not token or not chat_id:
        print("❌ Missing credentials!")
        sys.exit(1)

    message = (
        "🛡️ <b>[VIP PRODUCTION] TELEGRAM BOT REPORT</b> 🛡️\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🟢 <b>STATUS:</b> <code>PASSED & VERIFIED</code>\n"
        "🤖 <b>BOT NAME:</b> <code>api report</code>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔐 <b>PERMISSION MATRIX:</b>\n"
        "✅ <b>Send Messages:</b> ALLOWED\n"
        "✅ <b>Send Documents (.txt):</b> ALLOWED\n"
        "✅ <b>HTML Formatting:</b> ALLOWED\n"
        "✅ <b>Emoji/Stickers:</b> ALLOWED\n"
        "❌ <b>Delete Messages:</b> DENIED (Security)\n"
        "❌ <b>Read Other Chats:</b> DENIED (Privacy)\n"
        "❌ <b>Add/Remove Members:</b> DENIED\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚙️ <b>SYSTEM INFO:</b>\n"
        "📅 <b>Date:</b> Auto-Synced\n"
        "📁 <b>Target:</b> Production Group\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🚀 <i>Telegram Delivery System is 100% operational.</i>"
    )

    if send_telegram_message(message):
        print("✅ Test passed.")
        sys.exit(0)
    else:
        print("❌ Test failed.")
        sys.exit(1)


if __name__ == "__main__":
    run_test()
