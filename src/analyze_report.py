
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
REPORT_FILE = PROJECT_DIR / "reports" / "localhost_scan.txt"
SUMMARY_FILE = PROJECT_DIR / "reports" / "assessment_summary.txt"


def analyze_report():
    if not REPORT_FILE.exists():
        print("Scan report not found. Run local_scan.py first.")
        return

    report = REPORT_FILE.read_text(encoding="utf-8")

    open_ports = []

    for line in report.splitlines():
        parts = line.split()
        if len(parts) >= 3 and "/tcp" in parts[0] and parts[1] == "open":
            open_ports.append(
                f"Port: {parts[0]}, Service: {parts[2]}"
            )

    summary = [
        "ETHICAL HACKING LAB - ASSESSMENT SUMMARY",
        "=" * 42,
        "",
        "Target: 127.0.0.1 (local machine)",
        "Scope: Local TCP port and service scan",
        "",
        f"Open TCP ports detected: {len(open_ports)}",
    ]

    if open_ports:
        summary.extend(["", "Detected services:"])
        summary.extend(f"- {port}" for port in open_ports)
    else:
        summary.extend([
            "",
            "No open TCP ports were detected in the scan."
        ])

    summary.extend([
        "",
        "Important:",
        "- An open port is not automatically a vulnerability.",
        "- Review service configuration and software updates.",
        "- This summary is not a complete security audit.",
    ])

    SUMMARY_FILE.write_text(
        "\n".join(summary) + "\n",
        encoding="utf-8",
    )

    print("Assessment summary created successfully.")
    print(f"Saved to: {SUMMARY_FILE}")


if __name__ == "__main__":
    analyze_report()
