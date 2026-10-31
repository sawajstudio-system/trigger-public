import sys, os, requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    try:
        res = requests.get("https://text.pollinations.ai/Hello", timeout=15)
        send_telegram_message(f"✅ Pollinations Chat: {res.text[:50]}")
    except Exception as e: send_telegram_message(f"❌ Chat Error: {e}")
if __name__ == "__main__": run_test()
