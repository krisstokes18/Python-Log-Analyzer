# Python Log Analyzer

Reads authentication logs and summarizes failed login patterns by user and IP. Helps a junior analyst spot brute-force indicators and noisy accounts in minutes.

## Why It Matters
Security teams deal with high volumes of log data daily. This tool automates the manual process of scanning logs for suspicious patterns, reducing triage time and surfacing actionable indicators quickly.

## How to Run
1. Prerequisites: Python 3.x
2. Clone the repo: `git clone https://github.com/krisstokes18/Python-Log-Analyzer.git`
3. Navigate to folder: `cd Python-Log-Analyzer`
4. Run: `python log_analyzer.py sample.log --ips --out reports/summary.txt`
5. Expected output: summary report listing top IPs and flagged log lines

## Screenshots
See /docs for sample output screenshots.

## What I Learned
- Parsing log files using Python file I/O
- Extracting and counting IPs using dictionaries and regex
- Writing CLI tools with argument flags
- Generating structured summary reports from raw log data
- Connecting scripting skills to real SOC triage workflows

## Next Steps
- Add CSV export for summary output
- Build unit tests for edge cases including empty files and malformed lines
- Add timestamp filtering to narrow analysis to a specific time window

## Links
- LinkedIn: https://www.linkedin.com/in/kris-stokes-it/
