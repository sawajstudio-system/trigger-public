import sys, os, requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    try:
        res = requests.get("https://image.pollinations.ai/prompt/anime%20girl?model=flux-anime", timeout=60)
        send_telegram_message(f"✅ Flux Anime: Status {res.status_code}")
    except Exception as e: send_telegram_message(f"❌ Flux Anime Error: {e}")
if __name__ == "__main__": run_test()
