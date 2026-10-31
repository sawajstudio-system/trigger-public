import sys, os, requests
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
