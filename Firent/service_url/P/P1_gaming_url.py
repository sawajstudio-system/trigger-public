import sys, os, requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    res = requests.get("https://pokeapi.co/", timeout=15)
    send_telegram_message(f"✅ gaming: {res.status_code}")
if __name__ == "__main__": run_test()
