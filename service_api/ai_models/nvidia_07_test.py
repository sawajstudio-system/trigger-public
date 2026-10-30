import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Folder: API
# File: nvidia_07_test.py
import os
import sys
import requests
from service_api.integrations.telegram_01_helper import send_telegram_message

def run_test():
    api_key = os.getenv("NVIDIA_API_KEY")
    
    if not api_key:
        send_telegram_message("❌ <b>[PRODUCTION]</b> NVIDIA test failed: Secret missing.")
        sys.exit(1)

    # NVIDIA ke best free models ki list
    models_to_test = [
        "z-ai/glm-5.2",
        "moonshotai/kimi-k2.6",
        "nvidia/nemotron-3-ultra-550b-a55b"
    ]

    api_url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    success_model = None
    ai_reply = None
    failed_models = []

    print("🚀 Starting NVIDIA NIM Testing...")

    for model in models_to_test:
        print(f"⏳ Testing Model: {model}...")
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Say exactly: 'NVIDIA NIM is free and working!'"}],
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
            else:
                print(f"❌ Failed {model}: HTTP {res.status_code}")
                failed_models.append(f"{model} (HTTP {res.status_code})")
                
        except Exception as e:
            print(f"❌ Error with {model}: {str(e)}")
            failed_models.append(f"{model} (Error)")

    # Result Telegram par bhejna
    if success_model:
        message = (
            "🟩 <b>[VIP PRODUCTION] NVIDIA NIM REPORT</b> 🟩\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🟢 <b>STATUS:</b> <code>PASSED</code>\n"
            f"🏆 <b>WINNING MODEL:</b> <code>{success_model}</code>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💬 <b>AI REPLY:</b>\n<i>{ai_reply}</i>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⚠️ <b>Failed Models:</b> <code>{len(failed_models)}</code>\n"
            "🚀 <i>NVIDIA NIM is connected!</i>"
        )
        send_telegram_message(message)
        sys.exit(0)
    else:
        message = (
            "❌ <b>[PRODUCTION] NVIDIA NIM FAILED</b> ❌\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🔴 <b>STATUS:</b> <code>ALL MODELS FAILED</code>\n"
            "⚠️ <b>Reason:</b> API Key might be invalid.\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🛠️ <i>Please check your NVIDIA_API_KEY.</i>"
        )
        send_telegram_message(message)
        sys.exit(1)

if __name__ == "__main__":
    run_test()
