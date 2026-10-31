import sys, os, requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    try:
        res = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&limit=10", timeout=15)
        send_telegram_message(f"✅ AI Verified (e): Status {res.status_code}")
    except Exception as e: send_telegram_message(f"❌ Error: {e}")
if __name__ == "__main__": run_test()
