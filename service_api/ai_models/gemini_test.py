import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Folder: API
# File: gemini_test.py
import os
import sys
import requests
from service_api.integrations.telegram_helper import send_telegram_message

def run_test():
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        send_telegram_message("❌ <b>[PRODUCTION]</b> Gemini test failed: Secret missing.")
        sys.exit(1)

    # STEP 1: Google se poochho ki kaunse models abhi ZINDA hain
    print("🔍 Fetching available models from Google...")
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        res = requests.get(list_url, timeout=10)
        if res.status_code != 200:
            send_telegram_message(f"❌ API Key Error: Cannot fetch models. HTTP {res.status_code}")
            sys.exit(1)
            
        data = res.json()
        available_models = []
        
        # Sirf normal text generation models chuno (Deep Research hatao)
        for model in data.get("models", []):
            model_name = model.get("name", "").replace("models/", "")
            
            # Condition: Sirf wahi models lo jisme 'generateContent' ho AUR jo 'deep-research' na hon
            if "generateContent" in model.get("supportedGenerationMethods", []):
                if "deep-research" not in model_name and "embedding" not in model_name:
                    available_models.append(model_name)

        if not available_models:
            send_telegram_message("❌ No suitable text generation models found.")
            sys.exit(1)

        print(f"✅ Found {len(available_models)} usable models!")

    except Exception as e:
        send_telegram_message(f"❌ Network Error while fetching models: {str(e)}")
        sys.exit(1)

    # STEP 2: Ab normal models ko test karo
    success = False
    error_logs = []
    
    # Hum latest 5 normal models test karenge
    test_models = available_models[-5:] 
    
    for model in test_models:
        print(f"⏳ Testing Model: {model}...")
        
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": "Say 'System Online!'"}]}]
        }

        try:
            res = requests.post(api_url, json=payload, timeout=15)
            
            if res.status_code == 200:
                data = res.json()
                ai_reply = data['candidates'][0]['content']['parts'][0]['text']
                
                message = (
                    "🤖 <b>[VIP PRODUCTION] GEMINI AI REPORT</b> 🤖\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    "🟢 <b>STATUS:</b> <code>PASSED</code>\n"
                    f"🏆 <b>WINNING MODEL:</b> <code>{model}</code>\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"💬 <b>AI REPLY:</b>\n<i>{ai_reply}</i>\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    "🚀 <i>Google AI is connected and working.</i>"
                )
                send_telegram_message(message)
                sys.exit(0)
            else:
                err = f"{model} -> HTTP {res.status_code}"
                error_logs.append(err)
                print(f"❌ {err}")
                
        except Exception as e:
            err = f"{model} -> {str(e)}"
            error_logs.append(err)
            print(f"❌ {err}")

    # Agar saare normal models bhi fail ho gaye
    full_error = "\n".join(error_logs[:3]) # Sirf top 3 errors dikhao
    message = (
        "❌ <b>[PRODUCTION] GEMINI AI FAILED</b> ❌\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔴 <b>Status:</b> <code>QUOTA EXCEEDED / 429</code>\n"
        f"<i>{full_error}</i>\n"
        "🛠️ <i>Aapke account ki limit khatam hai. Google AI Studio mein billing enable karein.</i>"
    )
    send_telegram_message(message)
    sys.exit(1)

if __name__ == "__main__":
    run_test()
