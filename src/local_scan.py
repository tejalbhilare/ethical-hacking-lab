
import subprocess
from pathlib import Path
from datetime import datetime

# This assessment is restricted to your own computer.
TARGET = "127.0.0.1"

PROJECT_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_DIR / "reports"
REPORT_FILE = REPORT_DIR / "localhost_scan.txt"


def run_local_scan():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    print("Ethical Hacking Lab - Local Security Assessment")
    print(f"Authorized target: {TARGET}")
    print("Starting Nmap service scan...")

    try:
        result = subprocess.run(
            ["nmap", "-sV", TARGET],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )

        report = (
            "ETHICAL HACKING LAB - LOCAL ASSESSMENT\n"
            f"Scan date: {datetime.now().astimezone().isoformat()}\n"
            f"Target: {TARGET}\n"
            f"Nmap exit code: {result.returncode}\n\n"
            f"{result.stdout}\n"
            f"Errors, if any:\n{result.stderr}"
        )

        REPORT_FILE.write_text(report, encoding="utf-8")
        print("\nScan finished.")
        print(f"Report saved to: {REPORT_FILE}")

        if result.returncode != 0:
            print("Nmap reported an issue. Check the saved report.")

    except FileNotFoundError:
        print("Error: Nmap was not found. Check that Nmap is installed.")

    except subprocess.TimeoutExpired:
        print("Error: The scan took too long and was stopped.")


if __name__ == "__main__":
    run_local_scan()
