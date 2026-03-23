# Python Log Analyzer

## Why I Built This
Several job descriptions I was targeting — including roles at Snipes, 
Five Below, and PaulHood — listed Python scripting, log analysis, and 
automation as core responsibilities. I wanted to prove I could actually 
do it, not just list it as a skill. This was my first real Python 
project and I wanted to see how far I could take it.

## What It Does
This tool reads authentication log files from the command line, filters 
them by keyword, log level, or IP address, and surfaces the patterns 
that matter — failed logins, permission errors, suspicious IPs — in 
seconds instead of manually scanning through hundreds of lines. You can 
run it against one file or several at once and optionally save the 
output as a report.

## How I Built It
Built in Python using argparse for CLI flags, regex for level detection 
and IP extraction, and Counter for tallying results. The hardest part 
was getting the filters to work correctly — making sure a keyword or 
level flag only passed through the right lines without creating false 
positives, while still being flexible enough to handle different log 
formats.

## What I Learned
- Scripting can be as simple or as complex as you want it to be. 
  A basic log reader takes 20 lines. A flexible, production-style 
  CLI tool with error handling, multiple filters, and file output 
  takes considerably more thought.
- Generators are one-pass in Python — I had to reconstruct the 
  filter pipeline separately for IP counting, which forced me to 
  actually understand what was happening under the hood.
- The difference between writing code that works and writing code 
  that handles edge cases gracefully is where the real learning happens.

## Results
See /docs for screenshots showing a basic run, keyword and level 
filtering, IP extraction, and saved report output.

## What I'd Add Next
- CSV export for summary output
- Timestamp filtering to narrow analysis to a specific time window
- Unit tests for edge cases including empty files and malformed lines

## Links
- LinkedIn: https://www.linkedin.com/in/kris-stokes-it/
