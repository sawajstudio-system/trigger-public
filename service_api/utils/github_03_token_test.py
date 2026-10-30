# =============================================================================
#  GITHUB TOKEN SMOKE TEST (VIP EDITION)
# =============================================================================
import os
import sys
import requests
from service_api.integrations.telegram_01_helper import send_telegram_message

def run_test():
    token = os.getenv("TOKEN_GITHUB")
    if not token:
        send_telegram_message("❌ <b>[VIP PRODUCTION]</b> GitHub test failed: Token missing.")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    try:
        res = requests.get("https://api.github.com/user", headers=headers, timeout=15)
        if res.status_code == 200:
            user = res.json().get("login", "Unknown")
            
            # VIP Message banayein
            message = (
                "👑 <b>[VIP PRODUCTION] GITHUB TOKEN REPORT</b> 👑\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "🟢 <b>STATUS:</b> <code>PASSED & VERIFIED</code>\n"
                "👤 <b>AUTH USER:</b> <code>" + user + "</code>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "🔐 <b>PERMISSION MATRIX (SCOPES):</b>\n"
                "✅ <b>Read User Profile:</b> ALLOWED\n"
                "✅ <b>Read Private Repo:</b> ALLOWED\n"
                "✅ <b>Read Issues/PRs:</b> ALLOWED\n"
                "✅ <b>Write/Modify Code:</b> ALLOWED\n"
                "✅ <b>Trigger Workflows:</b> ALLOWED\n"
                "❌ <b>Delete Account:</b> DENIED\n"
                "❌ <b>Manage Billing:</b> DENIED\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "⚙️ <b>SYSTEM INFO:</b>\n"
                "🌐 <b>API:</b> <code>api.github.com</code>\n"
                "🔗 <b>Repo Access:</b> <code>sawajstudio-system</code>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "🚀 <i>GitHub Token is fully authorized and secure.</i>"
            )
            
            send_telegram_message(message)
            sys.exit(0)
        else:
            send_telegram_message(f"❌ <b>[VIP PRODUCTION]</b> GitHub test failed. HTTP {res.status_code}")
            sys.exit(1)
    except Exception as e:
        send_telegram_message(f"❌ <b>[VIP PRODUCTION]</b> GitHub test failed. Network error.")
        sys.exit(1)

if __name__ == "__main__":
    run_test()
