# Folder: API
# File: cloudinary_16_test.py
import os
import sys
import requests
from service_api.integrations.telegram_01_helper import send_telegram_message

def run_test():
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
    telegram_token = os.getenv("TELEGRAM_API_REPORT_TOKEN")
    chat_id = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")

    if not cloud_name:
        send_telegram_message("❌ <b>[PRODUCTION]</b> Cloudinary test failed: Cloud Name missing.")
        sys.exit(1)

    # 1. Ek test image generate karte hain (Pollinations AI se)
    prompt = "A futuristic cyberpunk city at night"
    image_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?width=512&height=512&nologo=true"
    
    print("⏳ Fetching LIVE image to upload...")
    img_res = requests.get(image_url, timeout=30)
    
    if img_res.status_code != 200:
        send_telegram_message("❌ <b>[PRODUCTION]</b> Failed to generate image for upload.")
        sys.exit(1)
        
    with open("temp_upload.jpg", "wb") as f:
        f.write(img_res.content)

    # 2. Cloudinary par direct upload (Unsigned)
    print("⏳ Uploading to Cloudinary...")
    upload_url = f"https://api.cloudinary.com/v1_1/{cloud_name}/image/upload"
    
    payload = {
        "upload_preset": "sawajstudio"  # <-- Aapka Cloudinary preset naam
    }
    
    files = {"file": open("temp_upload.jpg", "rb")}

    try:
        res = requests.post(upload_url, data=payload, files=files, timeout=30)
        
        if res.status_code == 200:
            data = res.json()
            secure_url = data.get("secure_url")
            
            message = (
                "☁️ <b>[VIP LIVE PRODUCTION] CLOUDINARY REPORT</b> ☁️\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "🟢 <b>STATUS:</b> <code>LIVE PASSED</code>\n"
                "🏆 <b>ACTION:</b> <code>Image Uploaded</code>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🔗 <b>LIVE URL:</b>\n<a href='{secure_url}'>Click to View Image</a>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "🚀 <i>Cloudinary Live System is connected!</i>"
            )
            send_telegram_message(message)
            print("✅ Cloudinary LIVE Upload successful!")
            sys.exit(0)
        else:
            error_msg = res.text[:200] 
            send_telegram_message(f"❌ <b>[LIVE FAILED]</b> Cloudinary failed. HTTP {res.status_code}\n<code>{error_msg}</code>")
            sys.exit(1)
            
    except Exception as e:
        send_telegram_message(f"❌ <b>[LIVE FAILED]</b> Cloudinary Network Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_test()
