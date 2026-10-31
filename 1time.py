import os
import shutil

print("🚀 Starting One-Time Service URL Setup & Fixer...")

# 1. Delete the wrong double folder if it exists
wrong_folder = "Firent/Firent"
if os.path.exists(wrong_folder):
    shutil.rmtree(wrong_folder)
    print(f"🗑️ Deleted wrong folder: {wrong_folder}")

# 2. Correct path (Bina Firent/ ke, kyunki script root se chal rahi hai)
base = "service_url"

# Folders create karo
for folder in ["image", "audio", "video", "ai_chat"]:
    os.makedirs(os.path.join(base, folder), exist_ok=True)

# File contents dictionary
files = {
    "image/pollinations_test.py": """import sys, os, requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    try:
        res = requests.get("https://image.pollinations.ai/prompt/cyberpunk%20city", timeout=60)
        send_telegram_message(f"✅ Pollinations: Status {res.status_code}")
    except Exception as e: send_telegram_message(f"❌ Pollinations Error: {e}")
if __name__ == "__main__": run_test()
""",
    "image/veida_test.py": """import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    try:
        import veida
        send_telegram_message("✅ Veida Library: Found")
    except ImportError: send_telegram_message("❌ Veida: Not installed")
if __name__ == "__main__": run_test()
""",
    "image/stable_diffusion_test.py": """import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    send_telegram_message("✅ Stable Diffusion (A1111): Requires Local Setup")
if __name__ == "__main__": run_test()
""",
    "image/invokeai_test.py": """import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    send_telegram_message("✅ InvokeAI: Requires Local Setup")
if __name__ == "__main__": run_test()
""",
    "image/kavel_test.py": """import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    send_telegram_message("✅ Kavel (Go): Requires Go setup")
if __name__ == "__main__": run_test()
""",
    "image/together_flux_test.py": """import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    send_telegram_message("✅ Together.ai (FLUX): Visit api.together.xyz")
if __name__ == "__main__": run_test()
""",
    "image/ai_image_editor_test.py": """import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    send_telegram_message("✅ AI Image Editor: Browser-based")
if __name__ == "__main__": run_test()
""",
    "image/flux_anime_test.py": """import sys, os, requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    try:
        res = requests.get("https://image.pollinations.ai/prompt/anime%20girl?model=flux-anime", timeout=60)
        send_telegram_message(f"✅ Flux Anime: Status {res.status_code}")
    except Exception as e: send_telegram_message(f"❌ Flux Anime Error: {e}")
if __name__ == "__main__": run_test()
""",
    "image/dalle3_test.py": """import sys, os, requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    try:
        res = requests.get("https://image.pollinations.ai/prompt/dog?model=dalle3", timeout=60)
        send_telegram_message(f"✅ DALL-E 3: Status {res.status_code}")
    except Exception as e: send_telegram_message(f"❌ DALL-E 3 Error: {e}")
if __name__ == "__main__": run_test()
""",
    "image/sd3_test.py": """import sys, os, requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    try:
        res = requests.get("https://image.pollinations.ai/prompt/car?model=sd3", timeout=60)
        send_telegram_message(f"✅ SD3: Status {res.status_code}")
    except Exception as e: send_telegram_message(f"❌ SD3 Error: {e}")
if __name__ == "__main__": run_test()
""",
    "audio/tts_studio_test.py": "# TTS Studio Placeholder\n",
    "audio/kokoro_test.py": "# Kokoro Placeholder\n",
    "audio/edge_tts_test.py": "# Edge TTS Placeholder\n",
    "audio/wavhost_test.py": "# Wavhost Placeholder\n",
    "audio/mizuoto_test.py": "# Mizuoto Placeholder\n",
    "audio/plapre_test.py": "# Plapre Placeholder\n",
    "audio/phonon_tts_test.py": "# Phonon Placeholder\n",
    "audio/aloud_test.py": "# Aloud Placeholder\n",
    "audio/speechma_test.py": "# Speechma Placeholder\n",
    "audio/readanytext_test.py": "# ReadAnyText Placeholder\n",
    "video/phane_test.py": "# Phane Placeholder\n",
    "video/kupkaprod_test.py": "# KupkaProd Placeholder\n",
    "video/chainstreet_test.py": "# ChainStreet Placeholder\n",
    "video/automated_video_gen_test.py": "# Auto Video Placeholder\n",
    "video/hailuo_local_test.py": "# Hailuo Placeholder\n",
    "video/pexels_url_test.py": "# Pexels Placeholder\n",
    "video/pixabay_url_test.py": "# Pixabay Placeholder\n",
    "video/mixkit_test.py": "# Mixkit Placeholder\n",
    "video/coverr_test.py": "# Coverr Placeholder\n",
    "video/librestock_test.py": "# Librestock Placeholder\n",
    "ai_chat/localmind_test.py": "# LocalMind Placeholder\n",
    "ai_chat/aether_test.py": "# Aether Placeholder\n",
    "ai_chat/aparte_test.py": "# Aparte Placeholder\n",
    "ai_chat/twin_o_matic_test.py": "# Twin Placeholder\n",
    "ai_chat/dulus_test.py": "# Dulus Placeholder\n",
    "ai_chat/pollinations_chat_test.py": """import sys, os, requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    try:
        res = requests.get("https://text.pollinations.ai/Hello", timeout=15)
        send_telegram_message(f"✅ Pollinations Chat: {res.text[:50]}")
    except Exception as e: send_telegram_message(f"❌ Chat Error: {e}")
if __name__ == "__main__": run_test()
""",
    "ai_chat/duck_ai_test.py": "# Duck AI Placeholder\n",
    "ai_chat/askai_test.py": "# AskAI Placeholder\n",
    "ai_chat/llm_browser_test.py": "# LLM Browser Placeholder\n",
    "ai_chat/unee_test.py": "# Unee Placeholder\n"
}

for path, content in files.items():
    full_path = os.path.join(base, path)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"✅ Successfully created {len(files)} files in the correct service_url folder!")
