import os
import requests

output_file = "combined_code.txt"
repos = ["Firent", "Backend"]

ignore_dirs = {".git", "node_modules", "venv", "__pycache__", ".github"}
ignore_exts = {".png", ".jpg", ".jpeg", ".zip", ".pdf", ".txt", ".exe"}

print("Dono repos ka code combine kiya ja raha hai...")

with open(output_file, "w", encoding="utf-8") as outfile:
    outfile.write("=== FIRENT & BACKEND BOTH REPOSITORIES CODE ===\n\n")

    for repo in repos:
        if not os.path.exists(repo):
            print(f"Folder nahi mila: {repo}")
            continue

        for root, dirs, files in os.walk(repo):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]

            for file in files:
                if any(file.endswith(ext) for ext in ignore_exts):
                    continue

                file_path = os.path.join(root, file)
                outfile.write("\n\n========================================\n")
                outfile.write(f"FILE: {file_path}\n")
                outfile.write("========================================\n\n")

                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"[Read Error: {e}]")

print("Telegram par file bheji ja rahi hai...")

token = os.environ.get("BOT_TOKEN")
chat_id = os.environ.get("CHAT_ID")
url = f"https://api.telegram.org/bot{token}/sendDocument"

with open(output_file, "rb") as f:
    files_payload = {"document": f}
    data_payload = {
        "chat_id": chat_id,
        "caption": "📁 Firent & Backend Dono Repositories ka Code (Manual Run)"
    }
    res = requests.post(url, data=data_payload, files=files_payload)

print("Response:", res.text)

if res.status_code == 200:
    print("Successfully sent to Telegram!")
else:
    print("Failed to send.")
