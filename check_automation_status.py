from datetime import datetime, timedelta
import subprocess

print("=== Automation Status Check ===")
print(f"Current time: {datetime.now()}")
print("Scheduled: Daily at 8:00 AM Berlin time")

# Check last automated run
result = subprocess.run(
    ["git", "log", "--grep=Automated", "-1", "--format=%ar - %s"],
    capture_output=True, text=True
)

if result.stdout:
    print(f"\nLast automated update: {result.stdout.strip()}")
else:
    print("\nNo automated updates found in git history")
    
print("\nTo verify automation is working:")
print("1. Check GitHub Actions tab in your repository")
print("2. Ensure GITHUB_TOKEN is set as repository secret")
print("3. Verify workflow has correct permissions")
