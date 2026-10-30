"""
cleanup.py
============
Purane GitHub Actions workflow runs ko delete karta hai.

Env vars (workflow se aayenge):
    GH_TOKEN        -> GitHub PAT (actions:write permission)
    REPO            -> owner/repo (jaise: user/Firent)
    CURRENT_RUN_ID  -> current run ID (ise skip karega)
    MAX_RUNS        -> max kitne runs fetch karne hain (default: 500)

Standalone run:
    export GH_TOKEN="ghp_xxx"
    export REPO="user/Firent"
    export CURRENT_RUN_ID=""
    python cleanup.py
"""

import os
import sys
import subprocess


def log(msg: str) -> None:
    print(msg, flush=True)


def run_gh(*args) -> subprocess.CompletedProcess:
    """gh CLI command chalata hai."""
    return subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        env=os.environ,
    )


def fetch_run_ids(repo: str, limit: int) -> list:
    """Workflow runs ki list fetch karta hai (sirf databaseId)."""
    result = run_gh(
        "run", "list",
        "--repo", repo,
        "--limit", str(limit),
        "--json", "databaseId",
        "--jq", ".[].databaseId",
    )

    if result.returncode != 0:
        log(f"❌ gh run list fail: {result.stderr.strip()}")
        return []

    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def delete_run(repo: str, run_id: str) -> bool:
    """Ek run delete karta hai."""
    result = run_gh("run", "delete", run_id, "--repo", repo)

    if result.returncode == 0:
        log(f"   🗑️  Deleted run ID: {run_id}")
        return True

    err = result.stderr.strip() or "unknown error"
    log(f"   ⚠️  Run {run_id} delete nahi hua: {err}")
    return False


def main() -> int:
    token = os.environ.get("GH_TOKEN")
    repo = os.environ.get("REPO")
    current_run_id = os.environ.get("CURRENT_RUN_ID", "").strip()
    max_runs = int(os.environ.get("MAX_RUNS", "500"))

    # ---- Validation ----
    if not token:
        log("❌ ERROR: GH_TOKEN missing hai.")
        return 1
    if not repo:
        log("❌ ERROR: REPO missing hai.")
        return 1

    log("=" * 60)
    log("🚀 Powerful Cleanup Process Shuru Ho Raha Hai...")
    log("=" * 60)
    log(f"   Repo           : {repo}")
    log(f"   Current run ID : {current_run_id or '(unknown)'}")
    log(f"   Max runs fetch : {max_runs}")
    log("")

    # ---- Fetch ----
    log(f"📥 {max_runs} tak runs fetch kar rahe hain...")
    run_ids = fetch_run_ids(repo, max_runs)

    if not run_ids:
        log("⚠️  Koi run nahi mila (ya list fail hui). Kuch delete nahi.")
        return 0

    log(f"✅ {len(run_ids)} runs mile.\n")

    # ---- Delete ----
    deleted = 0
    skipped = 0
    failed = 0

    for run_id in run_ids:
        if run_id == current_run_id:
            log(f"⚡ Skipping current active run ID: {run_id}")
            skipped += 1
            continue

        if delete_run(repo, run_id):
            deleted += 1
        else:
            failed += 1

    # ---- Summary ----
    log("\n" + "=" * 60)
    log("📊 Cleanup Summary")
    log("=" * 60)
    log(f"   🗑️  Deleted : {deleted}")
    log(f"   ⚡ Skipped : {skipped} (current run)")
    log(f"   ⚠️  Failed  : {failed}")
    log("=" * 60)

    if failed > 0:
        log("\n⚠️  Kuch runs delete nahi hue — permissions ya rate limit check karein.")

    log("\n✨ Cleanup complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
