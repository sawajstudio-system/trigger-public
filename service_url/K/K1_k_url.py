import sys, os, requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    try:
        res = requests.get("https://api.github.com", timeout=15)
        send_telegram_message(f"✅ AI Verified (k): Status {res.status_code}")
    except Exception as e: send_telegram_message(f"❌ Error: {e}")
if __name__ == "__main__": run_test()
