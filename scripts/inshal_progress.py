#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx>=0.28.1",
# ]
# ///
"""
Progress tracker for inshal.dev marked issues.

Fetches the live issue list from inshal.dev, parses fixed verses from
the current branch's diff and commit messages, and outputs a PR-ready
progress report.

Usage:
    python scripts/inshal_progress.py [--markdown] [--verbose]

Options:
    --markdown   Output full PR-ready markdown (default: summary table)
    --verbose    Show per-surah breakdown in summary mode
"""

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict

import httpx

ISSUES_URL = "https://inshal.dev/quran/marked/scanned_marked_verses.json"
VERSE_RE = re.compile(r"^(\d+)\|(\d+)\|")


def fetch_issues():
    resp = httpx.get(ISSUES_URL, timeout=15, follow_redirects=True)
    resp.raise_for_status()
    data = resp.json()
    return {entry["surah"]: sorted(entry["ayahs"]) for entry in data["surahs"]}


def _git(*args):
    return subprocess.check_output(["git"] + list(args), text=True).strip()


def get_merge_base():
    for candidate in [
        "dev",
        "origin/dev",
        "origin/master",
        "origin/main",
        "master",
        "main",
    ]:
        try:
            base = _git("merge-base", candidate, "HEAD")
            return base, candidate
        except subprocess.CalledProcessError:
            continue
    return None, None


def get_branch_diff_stats(base):
    raw = _git("diff", "--stat", f"{base}")
    files = []
    for line in raw.splitlines():
        m = re.match(r"\s*(.+?)\s*\|\s*(\d+)\s+(.+)", line)
        if m:
            files.append(
                {
                    "file": m.group(1).strip(),
                    "changes": int(m.group(2).strip()),
                    "detail": m.group(3).strip(),
                }
            )
    summary = re.search(r"(\d+) files? changed.*?(\d+) insertion.*?(\d+) deletion", raw)
    totals = None
    if summary:
        totals = {
            "files": int(summary.group(1)),
            "insertions": int(summary.group(2)),
            "deletions": int(summary.group(3)),
        }
    return files, totals


def get_changed_verses(base):
    diff = _git("diff", f"{base}", "--", "*.txt")
    changed = set()
    for line in diff.splitlines():
        if not line.startswith("+") or line.startswith("+++"):
            continue
        m = VERSE_RE.match(line[1:])
        if m:
            changed.add((int(m.group(1)), int(m.group(2))))
    return changed


def get_branch_commits(base):
    raw = _git("log", f"{base}..HEAD", "--format=%h %s")
    return raw.splitlines() if raw else []


def build_report(issues, fixed, changed_verses):
    all_issues = set()
    for surah, ayahs in issues.items():
        for ayah in ayahs:
            all_issues.add((surah, ayah))

    fixed_in_range = fixed & all_issues
    remaining = all_issues - fixed_in_range

    surah_fixed = defaultdict(set)
    surah_remaining = defaultdict(set)
    for s, a in fixed_in_range:
        surah_fixed[s].add(a)
    for s, a in remaining:
        surah_remaining[s].add(a)

    all_surahs = sorted(set(list(surah_fixed.keys()) + list(surah_remaining.keys())))

    return {
        "total": len(all_issues),
        "fixed": len(fixed_in_range),
        "remaining": len(remaining),
        "surahs": all_surahs,
        "surah_fixed": surah_fixed,
        "surah_remaining": surah_remaining,
        "changed_verses": changed_verses,
        "changed_in_issues": changed_verses & all_issues,
    }


def print_markdown(report, commits, diff_files, diff_totals):
    total = report["total"]
    fixed = report["fixed"]
    remaining = report["remaining"]
    pct = (fixed / total * 100) if total else 0

    print("## inshal.dev Issue Fix Progress\n")

    overall_bar_filled = int(pct / 5)
    overall_bar = "\u2588" * overall_bar_filled + "\u2591" * (20 - overall_bar_filled)
    print(f"**{fixed}/{total}** issues fixed ({pct:.1f}% complete)")
    print(f"**{overall_bar}**\n")

    if commits:
        print("### Commits on this branch\n")
        for c in commits:
            print(f"- `{c}`")
        print()

    if diff_totals:
        print("### Branch diff\n")
        print(
            f"**{diff_totals['files']} files changed**, "
            f"+{diff_totals['insertions']} / -{diff_totals['deletions']} lines\n"
        )
        print("| File | Changes |")
        print("|------|---------|")
        for f in diff_files:
            print(f"| `{f['file']}` | {f['changes']} ({f['detail']}) |")
        print()

    print("### Per-surah breakdown\n")
    print("| Surah | Fixed | Remaining | Progress |")
    print("|-------|-------|-----------|----------|")

    for s in report["surahs"]:
        sf = sorted(report["surah_fixed"].get(s, []))
        sr = sorted(report["surah_remaining"].get(s, []))
        total_s = len(sf) + len(sr)
        if total_s == 0:
            continue
        pct_s = len(sf) / total_s * 100
        bar_filled = int(pct_s / 10)
        bar = "\u2588" * bar_filled + "\u2591" * (10 - bar_filled)
        fixed_str = ", ".join(str(a) for a in sf) if sf else "-"
        remain_str = ", ".join(str(a) for a in sr) if sr else "-"
        print(f"| {s} | {fixed_str} | {remain_str} | {bar} {pct_s:.0f}% |")

    print()


def print_summary(report, verbose=False, base_name=None):
    total = report["total"]
    fixed = report["fixed"]
    remaining = report["remaining"]
    pct = (fixed / total * 100) if total else 0

    bar_len = 30
    filled = int(pct / 100 * bar_len)
    bar = "\u2588" * filled + "\u2591" * (bar_len - filled)

    print(f"inshal.dev progress: [{bar}] {fixed}/{total} ({pct:.1f}%)")
    if base_name:
        print(f"  Comparing against: {base_name}")
    print(f"  Fixed:     {fixed}")
    print(f"  Remaining: {remaining}")
    print(
        f"  Lines changed in branch: {len(report['changed_verses'])} verses "
        f"({len(report['changed_in_issues'])} touching inshal issues)"
    )

    if verbose:
        print()
        print("Per-surah breakdown:")
        for s in report["surahs"]:
            sf = sorted(report["surah_fixed"].get(s, []))
            sr = sorted(report["surah_remaining"].get(s, []))
            total_s = len(sf) + len(sr)
            if total_s == 0:
                continue
            pct_s = len(sf) / total_s * 100
            print(
                f"  Surah {s:>3}: {len(sf):>2}/{total_s:>2} ({pct_s:5.1f}%)  "
                f"remaining: {sr}"
            )


def main():
    parser = argparse.ArgumentParser(description="Track inshal.dev issue fix progress")
    parser.add_argument(
        "--markdown", action="store_true", help="Output PR-ready markdown"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Show per-surah breakdown"
    )
    args = parser.parse_args()

    try:
        issues = fetch_issues()
    except Exception as e:
        print(f"Error fetching issues from inshal.dev: {e}", file=sys.stderr)
        sys.exit(1)

    base, base_name = get_merge_base()
    if not base:
        print("Error: could not determine merge base", file=sys.stderr)
        sys.exit(1)

    changed_verses = get_changed_verses(base)
    report = build_report(issues, changed_verses, changed_verses)

    if args.markdown:
        commits = get_branch_commits(base)
        diff_files, diff_totals = get_branch_diff_stats(base)
        print_markdown(report, commits, diff_files, diff_totals)
    else:
        print_summary(report, verbose=args.verbose, base_name=base_name)


if __name__ == "__main__":
    main()
