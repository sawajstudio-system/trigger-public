import os

print("🚀 Starting All-in-One Real Platform Setup...")

# Path setup (Jahan files banani hain)
BASE_DIR = "Firent/service_url"

# Folders create karo
folders = ["translator", "voice", "background", "islamic"]
for f in folders:
    os.makedirs(os.path.join(BASE_DIR, f), exist_ok=True)

# ==========================================
# FILE CONTENTS (100% Real Platforms)
# ==========================================
files = {
    # 🌐 TRANSLATOR
    "translator/translators_lib_test.py": """import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    try:
        import translators as ts
        result = ts.translate_text("Hello world", translator='bing', from_language='en', to_language='hi')
        send_telegram_message(f"✅ Translators Lib (Real): {result}")
    except ImportError: send_telegram_message("⚠️ Translators lib not installed")
    except Exception as e: send_telegram_message(f"❌ Error: {e}")
if __name__ == "__main__": run_test()
""",
    
    # 🎙️ VOICE
    "voice/kokoro_tts_test.py": """import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    try:
        import kokoro
        send_telegram_message("✅ Kokoro TTS (Real): Library is installed.")
    except ImportError:
        send_telegram_message("⚠️ Kokoro TTS: Not installed")
    except Exception as e:
        send_telegram_message(f"❌ Error: {e}")
if __name__ == "__main__": run_test()
""",

    # 🖼️ BACKGROUND
    "background/openverse_test.py": """import sys, os, requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    try:
        url = "https://api.openverse.org/v1/images/?q=nature&page_size=1"
        res = requests.get(url, timeout=15)
        if res.status_code == 200:
            data = res.json().get("results", [])
            if data:
                send_telegram_message(f"✅ Openverse: Image Found")
            else:
                send_telegram_message("✅ Openverse: Working")
        else:
            send_telegram_message(f"❌ Openverse Failed: {res.status_code}")
    except Exception as e: send_telegram_message(f"❌ Error: {e}")
if __name__ == "__main__": run_test()
""",

    # 📖 ISLAMIC
    "islamic/quran_unified_test.py": """import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    try:
        import quran_unified
        send_telegram_message("✅ Quran Unified: Library installed")
    except ImportError:
        send_telegram_message("⚠️ Quran Unified: Not installed")
    except Exception as e:
        send_telegram_message(f"❌ Error: {e}")
if __name__ == "__main__": run_test()
"""
}

# File write loop
for path, content in files.items():
    full_path = os.path.join(BASE_DIR, path)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created: {full_path}")

print(f"\n🎉 Successfully created {len(files)} real platform files!")
