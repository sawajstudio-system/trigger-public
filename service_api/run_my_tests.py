# Folder: API
# File: run_my_tests.py
import os
import sys
import subprocess
import glob

def run_tests():
    print("🚀 [VIP SYSTEM] Starting Master Runner...")
    
    test_files = sorted(glob.glob("*_test.py"))
    target = os.getenv("TARGET_TEST", "all")
    
    if target != "all" and f"{target}.py" in test_files:
        test_files = [f"{target}.py"]

    failed = []
    passed = []

    # Aapke saare secrets ko environment variable mein save karna
    # taaki subprocess use padh sake
    env_vars = os.environ.copy()

    for test in test_files:
        print(f"▶️ Running: {test}")
        # Yahan hum env_vars pass kar rahe hain
        res = subprocess.run([sys.executable, test], env=env_vars)
        
        if res.returncode == 0:
            passed.append(test)
        else:
            failed.append(test)

    print(f"\n✅ Passed: {len(passed)} | ❌ Failed: {len(failed)}")
    if failed:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
