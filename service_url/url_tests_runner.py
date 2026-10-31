import os
import sys
import subprocess
import requests

def send_report(passed, failed):
    token = os.getenv("TELEGRAM_API_REPORT_TOKEN")
    chat_id = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")
    if not token or not chat_id: return

    msg = "🌍 <b>[URL SERVICE] FINAL TEST REPORT</b> 🌍\n"
    msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    if passed:
        msg += "✅ <b>PASSED:</b>\n"
        for p in passed:
            msg += f"  ✔️ <code>{p}</code>\n"
            
    if failed:
        msg += "\n❌ <b>FAILED:</b>\n"
        for f in failed:
            msg += f"  ❌ <code>{f}</code>\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"📊 <b>TOTAL:</b> {len(passed) + len(failed)} | ✅ {len(passed)} | ❌ {len(failed)}"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}, timeout=15)
        print("✅ Report sent to Telegram!")
    except Exception as e:
        print(f"❌ Report send failed: {e}")

def run_url_tests():
    print("🚀 Running all URL tests...")
    
    folders = ["image", "audio", "video", "ai_chat"]
    test_files = []
    
    # Saari test files dhoondho
    for folder in folders:
        if os.path.isdir(folder):
            for f in os.listdir(folder):
                if f.endswith("_test.py"):
                    test_files.append(os.path.join(folder, f))
                    
    if not test_files:
        print("⚠️ No test files found.")
        sys.exit(0)

    passed_tests = []
    failed_tests = []
    
    my_env = os.environ.copy()
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if parent_dir not in my_env.get("PYTHONPATH", ""):
        my_env["PYTHONPATH"] = f"{parent_dir}:{my_env.get('PYTHONPATH', '')}"

    for test_file in sorted(test_files):
        print(f"\n▶️ Running: {test_file}")
        result = subprocess.run([sys.executable, test_file], env=my_env)
        
        if result.returncode == 0:
            passed_tests.append(test_file)
            print(f"✅ PASSED: {test_file}")
        else:
            failed_tests.append(test_file)
            print(f"❌ FAILED: {test_file}")

    send_report(passed_tests, failed_tests)

    print("\n" + "="*40)
    print(f"✅ Passed: {len(passed_tests)} | ❌ Failed: {len(failed_tests)}")
    
    if len(failed_tests) > 2:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    run_url_tests()
