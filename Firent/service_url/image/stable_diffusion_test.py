import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    send_telegram_message("✅ Stable Diffusion (A1111): Requires Local Setup")
if __name__ == "__main__": run_test()
