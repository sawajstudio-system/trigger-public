import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Folder: API
# File: groq_06_test.py
import os
import sys
import requests
from service_api.integrations.telegram_01_helper import send_telegram_message

def run_test():
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        send_telegram_message("❌ <b>[PRODUCTION]</b> Groq test failed: Secret missing.")
        sys.exit(1)

    # Naye aur stable Groq models ki list
    models_to_test = [
        "openai/gpt-oss-120b",    # Sabse bada aur smart (Primary)
        "openai/gpt-oss-20b",     # Agar bada fail ho jaye toh backup
        "llama3-70b-8192",        # Backup (agar available ho)
        "llama3-8b-8192"          # Sabse fast backup
    ]

    success_model = None
    ai_reply = None
    failed_models = []
    
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    print("🚀 Starting Groq AI Model Testing...")

    # 1. LOOP: Ek-ek karke saare models test honge
    for model in models_to_test:
        print(f"⏳ Testing Model: {model}...")
        
        payload = {
            "model": model,
            "messages": [{
                "role": "user", 
                "content": "Reply with exactly this phrase: 'Groq is super fast and free!'"
            }],
            "max_tokens": 200,      # Tokens badha diye taaki reply pura aaye
            "temperature": 0.5      # Thoda creative but focused
        }

        try:
            res = requests.post(api_url, headers=headers, json=payload, timeout=15)
            
            if res.status_code == 200:
                data = res.json()
                ai_reply = data['choices'][0]['message']['content'].strip()
                success_model = model
                print(f"✅ Success with {model}!")
                break  # Model pass hua, loop se bahar
            else:
                print(f"❌ Failed {model}: HTTP {res.status_code}")
                failed_models.append(f"{model} (HTTP {res.status_code})")
                
        except Exception as e:
            print(f"❌ Error with {model}: {str(e)}")
            failed_models.append(f"{model} (Error)")

    # 2. RESULT BHEJNA
    if success_model:
        # Agar koi model pass hua
        message = (
            "⚡ <b>[VIP PRODUCTION] GROQ AI REPORT</b> ⚡\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🟢 <b>STATUS:</b> <code>PASSED</code>\n"
            f"🏆 <b>WINNING MODEL:</b> <code>{success_model}</code>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💬 <b>AI REPLY:</b>\n<i>{ai_reply}</i>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⚠️ <b>Failed Models:</b> <code>{len(failed_models)}</code>\n"
            "🚀 <i>Groq is connected and working without a card!</i>"
        )
        send_telegram_message(message)
        sys.exit(0)
    else:
        # Agar saare models fail ho gaye
        message = (
            "❌ <b>[PRODUCTION] GROQ AI FAILED</b> ❌\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🔴 <b>STATUS:</b> <code>ALL MODELS FAILED</code>\n"
            "⚠️ <b>Reason:</b> API Key might be invalid or limit exceeded.\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🛠️ <i>Please check your GROQ_API_KEY in GitHub Secrets.</i>"
        )
        send_telegram_message(message)
        sys.exit(1)

if __name__ == "__main__":
    run_test()
