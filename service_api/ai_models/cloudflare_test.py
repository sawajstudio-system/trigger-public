import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Folder: API
# File: cloudflare_test.py
import os
import sys
import requests
from service_api.integrations.telegram_01_helper import send_telegram_message

def run_test():
    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    api_token = os.getenv("CLOUDFLARE_API_TOKEN")
    
    if not account_id or not api_token:
        send_telegram_message("❌ <b>[PRODUCTION]</b> Cloudflare test failed: Secret missing.")
        sys.exit(1)

    # Ye line automatically GitHub Secret se Account ID utha legi
    api_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/meta/llama-3.1-8b-instruct"
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [
            {"role": "user", "content": "Say exactly: 'Cloudflare AI is free and working!'"}
        ]
    }

    try:
        res = requests.post(api_url, headers=headers, json=payload, timeout=20)
        
        if res.status_code == 200:
            data = res.json()
            ai_reply = data.get('result', {}).get('response', 'No reply')
            
            message = (
                "☁️ <b>[VIP PRODUCTION] CLOUDFLARE AI REPORT</b> ☁️\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "🟢 <b>STATUS:</b> <code>PASSED</code>\n"
                "🏆 <b>MODEL:</b> <code>llama-3.1-8b-instruct</code>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"💬 <b>AI REPLY:</b>\n<i>{ai_reply}</i>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "🚀 <i>Cloudflare is connected!</i>"
            )
            send_telegram_message(message)
            sys.exit(0)
        else:
            send_telegram_message(f"❌ <b>[PRODUCTION]</b> Cloudflare test failed.\nHTTP {res.status_code}\n<code>{res.text[:150]}</code>")
            sys.exit(1)
            
    except Exception as e:
        send_telegram_message(f"❌ <b>[PRODUCTION]</b> Cloudflare test failed. Network Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_test()
