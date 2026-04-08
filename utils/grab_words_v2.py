#!/usr/bin/env python

import collections
import csv
import re
from pathlib import Path

ARAB_SET = "\u0621-\u06ff"
THAA_SET = "\u0780-\u07b1"

BASE_DIR = Path(__file__).resolve().parent.parent
TRANS_FILE = BASE_DIR / "master_dv.divehi.txt"
FREQ_CSV = BASE_DIR / "utils/transliterator/transliteration_data/_quran_freq_dv.csv"
NEXT_WORDS_CSV = (
    BASE_DIR / "utils/transliterator/transliteration_data/_dhivehi_next_words.csv"
)

ARABIC_RE = re.compile(f"[{ARAB_SET}][{ARAB_SET} ]+[{ARAB_SET}]?")
COMBO_RE = re.compile(rf"(?<!\w)[{ARAB_SET}][{ARAB_SET} ]+[{THAA_SET}]+")
SPLIT_RE = re.compile(f"([{ARAB_SET}][{ARAB_SET} ]+[{ARAB_SET}]?) ([{THAA_SET}]+)")


def read_translation_lines():
    with TRANS_FILE.open(encoding="utf-8") as f:
        return f.readlines()


def extract_arabic_frequencies(lines):
    words = []
    for line in lines:
        words.extend(m.strip() for m in ARABIC_RE.findall(line))
    return collections.Counter(words)


def extract_next_word_frequencies(lines):
    words = []
    for line in lines:
        words.extend(
            split.group(2)
            for combo in COMBO_RE.finditer(line)
            if (split := SPLIT_RE.match(combo[0]))
        )
    return collections.Counter(words)


def read_csv_rows(path, fieldnames):
    rows = []
    if path.exists():
        with path.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                filled = {field: row.get(field, "") for field in fieldnames}
                rows.append(filled)
    return rows


def write_csv(path, fieldnames, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def update_csv(path, fieldnames, key_field, new_freqs):
    existing_rows = read_csv_rows(path, fieldnames)
    existing_by_key = {row[key_field]: row for row in existing_rows}

    new_count = 0
    updated_count = 0
    new_rows = []

    for word, freq in new_freqs.items():
        if word in existing_by_key:
            old_freq = existing_by_key[word].get("freq", "")
            if old_freq != str(freq):
                existing_by_key[word]["freq"] = str(freq)
                updated_count += 1
        else:
            new_row = dict.fromkeys(fieldnames, "")
            new_row[key_field] = word
            new_row["freq"] = str(freq)
            new_rows.append(new_row)
            new_count += 1

    existing_rows.extend(new_rows)
    write_csv(path, fieldnames, existing_rows)
    return new_count, updated_count, len(existing_rows)


def main():
    lines = read_translation_lines()

    ar_freqs = extract_arabic_frequencies(lines)
    ar_new, ar_updated, ar_total = update_csv(
        FREQ_CSV,
        ["ar", "dv", "freq", "unchangable", "alt_spelling", "comment"],
        "ar",
        ar_freqs,
    )

    nw_freqs = extract_next_word_frequencies(lines)
    nw_new, nw_updated, nw_total = update_csv(
        NEXT_WORDS_CSV,
        ["word", "freq", "joinable", "trim_first_letter"],
        "word",
        nw_freqs,
    )

    print("=== _quran_freq_dv.csv ===")
    print(f"  New Arabic words: {ar_new}")
    print(f"  Updated frequencies: {ar_updated}")
    print(f"  Total rows: {ar_total}")
    print()
    print("=== _dhivehi_next_words.csv ===")
    print(f"  New next-words: {nw_new}")
    print(f"  Updated frequencies: {nw_updated}")
    print(f"  Total rows: {nw_total}")


if __name__ == "__main__":
    main()
