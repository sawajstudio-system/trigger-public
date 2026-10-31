import sys, os, requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    try:
        res = requests.get("https://image.pollinations.ai/prompt/car?model=sd3", timeout=60)
        send_telegram_message(f"✅ SD3: Status {res.status_code}")
    except Exception as e: send_telegram_message(f"❌ SD3 Error: {e}")
if __name__ == "__main__": run_test()
