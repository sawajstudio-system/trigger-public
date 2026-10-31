import sys, os, requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    try:
        res = requests.get("https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true", timeout=15)
        send_telegram_message(f"✅ Verified (Weather API): Status {res.status_code}")
    except Exception as e: send_telegram_message(f"❌ Error: {e}")
if __name__ == "__main__": run_test()
