import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Folder: API
# File: anges_test.py
import os
import sys
import requests
from service_api.integrations.telegram_helper import send_telegram_message

def run_test():
    api_key = os.getenv("ANGES_API_KEY")
    
    if not api_key:
        send_telegram_message("❌ <b>[PRODUCTION]</b> Anges AI test failed: ANGES_API_KEY missing.")
        sys.exit(1)

    # Sahi Base URL (apihub ke saath)
    api_url = "https://apihub.agnes-ai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Naya Model Name
    payload = {
        "model": "agnes-2.5-flash",
        "messages": [{"role": "user", "content": "Say exactly: 'Anges AI is working!'"}],
        "max_tokens": 100
    }

    try:
        res = requests.post(api_url, headers=headers, json=payload, timeout=20)
        
        if res.status_code == 200:
            data = res.json()
            ai_reply = data['choices'][0]['message']['content'].strip()
            
            message = (
                "🧠 <b>[VIP PRODUCTION] ANGES AI REPORT</b> 🧠\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "🟢 <b>STATUS:</b> <code>PASSED</code>\n"
                "🏆 <b>MODEL:</b> <code>agnes-2.5-flash</code>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"💬 <b>AI REPLY:</b>\n<i>{ai_reply}</i>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "🚀 <i>Anges AI is connected!</i>"
            )
            send_telegram_message(message)
            sys.exit(0)
        else:
            send_telegram_message(f"❌ <b>[PRODUCTION]</b> Anges AI failed.\nHTTP {res.status_code}\n<code>{res.text[:150]}</code>")
            sys.exit(1)
            
    except Exception as e:
        send_telegram_message(f"❌ <b>[PRODUCTION]</b> Anges AI Network Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_test()
