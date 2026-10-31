import sys, os
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
