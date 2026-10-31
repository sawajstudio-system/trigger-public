import sys, os
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
