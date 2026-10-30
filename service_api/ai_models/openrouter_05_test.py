import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Folder: API
# File: openrouter_05_test.py
import os
import sys
import requests
from service_api.integrations.telegram_01_helper import send_telegram_message

def run_test():
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        send_telegram_message("❌ <b>[PRODUCTION]</b> OpenRouter test failed: Secret missing.")
        sys.exit(1)

    # Smart Model List (jo abhi active hain)
    models_to_test = [
        "openai/gpt-oss-120b:free",
        "qwen/qwen3.6-plus:free",
        "google/gemma-4-31b-it:free",
        "openrouter/free"  # Auto-select backup
    ]

    api_url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    success_model = None
    ai_reply = None
    limit_hit = False  # Track karein agar limit khatam ho

    print("🚀 Starting OpenRouter Testing...")

    for model in models_to_test:
        print(f"⏳ Testing Model: {model}...")
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Say exactly: 'OpenRouter is free and working!'"}],
            "max_tokens": 100
        }

        try:
            res = requests.post(api_url, headers=headers, json=payload, timeout=20)
            
            if res.status_code == 200:
                data = res.json()
                ai_reply = data['choices'][0]['message']['content'].strip()
                success_model = model
                print(f"✅ Success with {model}!")
                break
            elif res.status_code == 429:
                # Limit khatam ho gayi
                print(f"⚠️ Rate limit hit on {model}")
                limit_hit = True
                # Agar limit hit hui toh loop break kar do, aage try mat karo
                break
            else:
                print(f"❌ Failed {model}: HTTP {res.status_code}")
                
        except Exception as e:
            print(f"❌ Error with {model}: {str(e)}")

    # Result Bhejna
    if success_model:
        message = (
            "🌐 <b>[VIP PRODUCTION] OPENROUTER AI REPORT</b> 🌐\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🟢 <b>STATUS:</b> <code>PASSED</code>\n"
            f"🏆 <b>WINNING MODEL:</b> <code>{success_model}</code>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💬 <b>AI REPLY:</b>\n<i>{ai_reply}</i>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🚀 <i>OpenRouter is connected!</i>"
        )
        send_telegram_message(message)
        sys.exit(0)
        
    elif limit_hit:
        # Limit khatam hai, lekin crash nahi hoga
        message = (
            "⏳ <b>[PRODUCTION] OPENROUTER LIMIT REACHED</b> ⏳\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🔴 <b>STATUS:</b> <code>QUOTA EXHAUSTED</code>\n"
            "⚠️ <b>Reason:</b> Free tier limit (50 requests/day) khatam ho gayi hai.\n"
            "📅 <b>Reset Time:</b> <code>UTC Midnight (5:30 AM IST)</code>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🛠️ <i>Kal wapas try karein ya $10 credit add karein.</i>"
        )
        send_telegram_message(message)
        sys.exit(0) # Exit 0 taaki workflow fail na ho
        
    else:
        message = (
            "❌ <b>[PRODUCTION] OPENROUTER AI FAILED</b> ❌\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🔴 <b>STATUS:</b> <code>ALL MODELS FAILED</code>\n"
            "⚠️ <b>Reason:</b> API Key might be invalid.\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🛠️ <i>Please check your OPENROUTER_API_KEY in GitHub Secrets.</i>"
        )
        send_telegram_message(message)
        sys.exit(1)

if __name__ == "__main__":
    run_test()
