import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Folder: API
# File: cohere_test.py
import os
import sys
import requests
from service_api.integrations.telegram_helper import send_telegram_message

def run_test():
    api_key = os.getenv("COHERE_API_KEY")
    
    if not api_key:
        send_telegram_message("❌ <b>[PRODUCTION]</b> Cohere test failed: Secret missing.")
        sys.exit(1)

    api_url = "https://api.cohere.com/v1/chat"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Naye active models ki list
    models_to_test = [
        "command-r-plus-08-2024",
        "command-r-08-2024",
        "command-light"
    ]

    success_model = None
    ai_reply = None
    failed_models = []

    print("🚀 Starting Cohere AI Testing...")

    for model in models_to_test:
        print(f"⏳ Testing Model: {model}...")
        
        payload = {
            "model": model,
            "message": "Say exactly: 'Cohere is free and working!'",
            "max_tokens": 50
        }

        try:
            res = requests.post(api_url, headers=headers, json=payload, timeout=20)
            
            if res.status_code == 200:
                data = res.json()
                ai_reply = data.get("text", "No reply")
                success_model = model
                print(f"✅ Success with {model}!")
                break
            else:
                print(f"❌ Failed {model}: HTTP {res.status_code}")
                failed_models.append(f"{model} (HTTP {res.status_code})")
                
        except Exception as e:
            print(f"❌ Error with {model}: {str(e)}")
            failed_models.append(f"{model} (Error)")

    # Result Telegram par bhejna
    if success_model:
        message = (
            "🇨🇦 <b>[VIP PRODUCTION] COHERE AI REPORT</b> 🇨🇦\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🟢 <b>STATUS:</b> <code>PASSED</code>\n"
            f"🏆 <b>WINNING MODEL:</b> <code>{success_model}</code>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💬 <b>AI REPLY:</b>\n<i>{ai_reply}</i>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⚠️ <b>Failed Models:</b> <code>{len(failed_models)}</code>\n"
            "🚀 <i>Cohere is connected!</i>"
        )
        send_telegram_message(message)
        sys.exit(0)
    else:
        message = (
            "❌ <b>[PRODUCTION] COHERE AI FAILED</b> ❌\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🔴 <b>STATUS:</b> <code>ALL MODELS FAILED</code>\n"
            "⚠️ <b>Reason:</b> API Key might be invalid or rate limit.\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🛠️ <i>Please check your COHERE_API_KEY.</i>"
        )
        send_telegram_message(message)
        sys.exit(1)

if __name__ == "__main__":
    run_test()
