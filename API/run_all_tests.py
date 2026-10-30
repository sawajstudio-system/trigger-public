# Folder: API
# File: run_all_tests.py
import os
import sys
import subprocess
import glob
import requests

def send_final_report(passed, failed):
    token = os.getenv("TELEGRAM_API_REPORT_TOKEN")
    chat_id = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")
    if not token or not chat_id: return

    msg = "👑 <b>[VIP PRODUCTION] FINAL TEST REPORT</b> 👑\n"
    msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    if passed:
        msg += "✅ <b>PASSED:</b>\n"
        for p in passed:
            msg += f"  ✔️ <code>{p.replace('_test.py', '').replace('.py', '')}</code>\n"
            
    if failed:
        msg += "\n❌ <b>FAILED:</b>\n"
        for f in failed:
            msg += f"  ❌ <code>{f.replace('_test.py', '').replace('.py', '')}</code>\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"📊 <b>TOTAL:</b> {len(passed) + len(failed)} | ✅ {len(passed)} | ❌ {len(failed)}"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"})
    except:
        pass

def run_all():
    print("🚀 [VIP SYSTEM] Auto-running all tests...")
    test_files = sorted(glob.glob("*_test.py"))
    
    if os.path.exists("image_creator.py"):
        test_files.append("image_creator.py")

    if not test_files:
        print("⚠️ No test files found.")
        sys.exit(0)

    failed_tests = []
    passed_tests = []
    
    # 🛠️ Yahan secrets ko copy kiya jaa raha hai
    my_env = os.environ.copy()

    for test_file in test_files:
        print(f"\n▶️ Running: {test_file}")
        # 🛠️ Yahan env pass kiya jaa raha hai, isse cloudinary ko keys mil jayengi
        result = subprocess.run([sys.executable, test_file], env=my_env)
        
        if result.returncode == 0:
            passed_tests.append(test_file)
            print(f"✅ PASSED: {test_file}")
        else:
            failed_tests.append(test_file)
            print(f"❌ FAILED: {test_file}")

    send_final_report(passed_tests, failed_tests)

    print("\n" + "="*40)
    print(f"✅ Passed: {len(passed_tests)} | ❌ Failed: {len(failed_tests)}")
    
    if failed_tests:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    run_all()
