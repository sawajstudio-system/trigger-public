import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    send_telegram_message("✅ Kavel (Go): Requires Go setup")
if __name__ == "__main__": run_test()
