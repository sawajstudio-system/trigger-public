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
            test_name = os.path.basename(p).replace('_test.py', '').replace('.py', '')
            msg += f"  ✔️ <code>{test_name}</code>\n"
            
    if failed:
        msg += "\n❌ <b>FAILED:</b>\n"
        for f in failed:
            test_name = os.path.basename(f).replace('_test.py', '').replace('.py', '')
            msg += f"  ❌ <code>{test_name}</code>\n"
            
    msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"📊 <b>TOTAL:</b> {len(passed) + len(failed)} | ✅ {len(passed)} | ❌ {len(failed)}"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"})
    except:
        pass

def run_all():
    print("🚀 [VIP SYSTEM] Auto-running all tests recursively from subfolders...")
    
    # Recursive globbing taaki subfolders ke andar ki saari test files mil jayein
    test_files = sorted(glob.glob("**/*_test.py", recursive=True))
    
    if os.path.exists("image_creator.py"):
        test_files.append("image_creator.py")

    if not test_files:
        print("⚠️ No test files found.")
        sys.exit(0)

    failed_tests = []
    passed_tests = []
    
    my_env = os.environ.copy()
    current_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
    if parent_dir not in my_env.get("PYTHONPATH", ""):
        my_env["PYTHONPATH"] = f"{parent_dir}:{my_env.get('PYTHONPATH', '')}"

    for test_file in test_files:
        print(f"\n▶️ Running: {test_file}")
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
