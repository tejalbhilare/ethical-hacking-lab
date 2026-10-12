# Ethical Hacking Lab and Vulnerability Assessment System

## Project Overview

This project demonstrates basic ethical hacking and security assessment concepts in a controlled local environment. It uses Nmap to identify open TCP ports and detect running services, then uses Python to generate a readable assessment summary.

## Objectives

- Learn basic network scanning using Nmap.
- Identify open TCP ports and detected services on a local machine.
- Process scan reports using Python.
- Generate a structured security assessment summary.
- Understand the difference between an open port and a confirmed vulnerability.

## Technologies Used

- **Python** — report processing and summary generation.
- **Nmap** — local port scanning and service detection.
- **Ubuntu on WSL** — Linux lab environment.
- **Git and GitHub** — version control and project hosting.

## Project Structure

```text
ethical-hacking-lab/
├── data/
├── docs/
├── reports/
│   ├── localhost_scan.txt
│   └── assessment_summary.txt
├── screenshots/
├── src/
│   ├── local_scan.py
│   └── analyze_report.py
├── .venv/
└── README.md
```

## How to Run

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Run the local scan:

```bash
python src/local_scan.py
```

Generate the assessment summary:

```bash
python src/analyze_report.py
```

The generated reports are saved in the `reports/` directory.

## Current Test Result

The initial local scan detected TCP port 22 running SSH on `127.0.0.1`. An open port does not automatically indicate a vulnerability; further configuration and security checks are required.

## Ethical Use and Scope

This project is configured to scan only `127.0.0.1`, the local machine. Testing other systems requires explicit authorization and a clearly defined scope.

## Future Improvements

- Add a dashboard to display scan findings.
- Improve report parsing and error handling.
- Add security recommendations based on verified findings.
- Test additional checks in an isolated, intentionally vulnerable lab.
- Add screenshots and a detailed project report.

## Disclaimer

This is an educational project. Its results are not a substitute for a professional security audit.
