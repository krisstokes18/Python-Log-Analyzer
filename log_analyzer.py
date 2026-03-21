#!/usr/bin/env python3
"""
Tiny Log Analyzer (CLI+)
- Read one or more files (or --stdin)
- Optional keyword and level filters
- Count repeated lines; show top N
- Extract and count IPs
- Optional report output to a file
"""
from __future__ import annotations
import sys, re, argparse
from pathlib import Path
from collections import Counter
from typing import Iterable, Iterator, Sequence

LEVEL_RE = re.compile(r"\b(ERROR|WARN|WARNING|INFO|DEBUG|CRITICAL)\b", re.IGNORECASE)
IP_RE    = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

def iter_lines(paths: Sequence[Path]) -> Iterator[str]:
    """Yield lines from all files (utf-8), skipping unreadable ones with a warning."""
    for p in paths:
        try:
            with p.open("r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    yield line.rstrip("\n")
        except FileNotFoundError:
            print(f"[WARN] Missing file: {p}", file=sys.stderr)
        except OSError as e:
            print(f"[WARN] Could not read {p}: {e}", file=sys.stderr)

def filter_keyword(lines: Iterable[str], keyword: str, ignore_case: bool) -> Iterator[str]:
    if not keyword:
        yield from lines
        return
    if ignore_case:
        kw = keyword.lower()
        for ln in lines:
            if kw in ln.lower():
                yield ln
    else:
        for ln in lines:
            if keyword in ln:
                yield ln

def filter_level(lines: Iterable[str], level: str | None) -> Iterator[str]:
    if not level:
        yield from lines
        return
    lvl = level.upper()
    for ln in lines:
        m = LEVEL_RE.search(ln)
        if m and m.group(1).upper().startswith(lvl):  # "WARN" matches "WARNING"
            yield ln

def count_lines(lines: Iterable[str]) -> Counter[str]:
    c = Counter()
    for ln in lines:
        if ln.strip():
            c[ln] += 1
    return c

def count_ips(lines: Iterable[str]) -> Counter[str]:
    c = Counter()
    for ln in lines:
        for ip in IP_RE.findall(ln):
            c[ip] += 1
    return c

def format_table(title: str, pairs: Sequence[tuple[str,int]], width: int = 60) -> str:
    out = [f"=== {title} ==="]
    for k, v in pairs:
        left = (k[:width-10] + "…") if len(k) > width-3 else k
        out.append(f"{left.ljust(width)} {v}")
    return "\n".join(out)

def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Tiny Log Analyzer (CLI+)")
    ap.add_argument("paths", nargs="*", help="Log file paths (accepts globs on most shells)")
    ap.add_argument("--stdin", action="store_true", help="Read from STDIN instead of files")
    ap.add_argument("--keyword", help="Only count lines containing this keyword")
    ap.add_argument("--ignore-case", action="store_true", help="Case-insensitive keyword match")
    ap.add_argument("--level", choices=["ERROR","WARN","WARNING","INFO","DEBUG","CRITICAL"],
                    help="Filter by detected level")
    ap.add_argument("--top", type=int, default=10, help="Show top N results (default: 10)")
    ap.add_argument("--ips", action="store_true", help="Extract and count IPv4 addresses")
    ap.add_argument("--out", type=Path, help="Write report to this file instead of stdout")
    args = ap.parse_args(argv)

    # Collect input lines
    if args.stdin:
        src_lines = (ln.rstrip("\n") for ln in sys.stdin)
    else:
        if not args.paths:
            ap.error("Provide at least one path or use --stdin")
        paths = [Path(p) for p in args.paths]
        src_lines = iter_lines(paths)

    # Apply filters in sequence
    ln1 = filter_keyword(src_lines, args.keyword or "", args.ignore_case)
    ln2 = filter_level(ln1, args.level)

    # Count lines and (optionally) IPs
    line_counts = count_lines(ln2)
    top_lines = line_counts.most_common(args.top)

    # For IP counting, we must re-run filters over source (generators are one-pass).
    # Reconstruct pipeline:
    if args.stdin:
        # If reading from stdin, we already consumed it; warn and skip IPs
        ip_counts = Counter()
        if args.ips:
            print("[WARN] --ips ignored with --stdin (stream already consumed). Pipe twice if needed.", file=sys.stderr)
    else:
        paths = [Path(p) for p in args.paths]
        ln_ip = filter_level(filter_keyword(iter_lines(paths), args.keyword or "", args.ignore_case), args.level)
        ip_counts = count_ips(ln_ip) if args.ips else Counter()

    # Build report text
    report_parts = []
    report_parts.append(format_table("Top Lines", top_lines))
    if args.ips:
        report_parts.append(format_table("Top IPs", ip_counts.most_common(args.top)))
    report = "\n\n".join(report_parts) + "\n"

    # Output
    if args.out:
        try:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(report, encoding="utf-8")
            print(f"[OK] Wrote report -> {args.out}")
        except OSError as e:
            print(f"[ERROR] Could not write report: {e}", file=sys.stderr)
            print(report)  # fallback to stdout
    else:
        print(report)

    return 0

if __name__ == "__main__":
    print(main())
