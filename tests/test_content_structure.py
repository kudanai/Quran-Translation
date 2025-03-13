from . import QuranCorpus


def test_line_count():
    """
    Number of lines in translation files must == 6236
    """
    lines = list(QuranCorpus.read_lines())
    assert len(lines) == 6236, f"Expected 6236 lines, got {len(lines)}"


def test_line_format():
    """
    Ensure each line follows the expected format: sura|ayat|translation
    with valid sura and ayat numbers
    """
    for line in QuranCorpus.read_lines():
        parts = line.split("|")
        assert len(parts) == 3, f"Line does not have 3 parts: {line[:50]}..."
        assert parts[0].isdigit(), f"Sura is not a number: {parts[0]}"
        assert parts[1].isdigit(), f"Ayat is not a number: {parts[1]}"
        assert int(parts[0]) >= 1 and int(parts[0]) <= 114, f"Invalid sura number: {parts[0]}"


def test_no_empty_translations():
    """
    Ensure no translation is empty or just whitespace
    """
    for line in QuranCorpus.read_lines():
        _, _, translation = line.split("|")
        assert translation.strip(), f"Empty translation found in line: {line[:50]}..."


def test_sura_verse_counts():
    """
    Verify that each sura has the correct number of verses according to standard Quran
    """
    # Standard verse counts for each sura, extracted from quran-json
    standard_verse_counts = {
        1: 7, 2: 286, 3: 200, 4: 176, 5: 120, 6: 165, 7: 206, 8: 75, 9: 129,
        10: 109, 11: 123, 12: 111, 13: 43, 14: 52, 15: 99, 16: 128, 17: 111, 18: 110,
        19: 98, 20: 135, 21: 112, 22: 78, 23: 118, 24: 64, 25: 77, 26: 227, 27: 93,
        28: 88, 29: 69, 30: 60, 31: 34, 32: 30, 33: 73, 34: 54, 35: 45, 36: 83,
        37: 182, 38: 88, 39: 75, 40: 85, 41: 54, 42: 53, 43: 89, 44: 59, 45: 37,
        46: 35, 47: 38, 48: 29, 49: 18, 50: 45, 51: 60, 52: 49, 53: 62, 54: 55,
        55: 78, 56: 96, 57: 29, 58: 22, 59: 24, 60: 13, 61: 14, 62: 11, 63: 11,
        64: 18, 65: 12, 66: 12, 67: 30, 68: 52, 69: 52, 70: 44, 71: 28, 72: 28,
        73: 20, 74: 56, 75: 40, 76: 31, 77: 50, 78: 40, 79: 46, 80: 42, 81: 29,
        82: 19, 83: 36, 84: 25, 85: 22, 86: 17, 87: 19, 88: 26, 89: 30, 90: 20,
        91: 15, 92: 21, 93: 11, 94: 8, 95: 8, 96: 19, 97: 5, 98: 8, 99: 8,
        100: 11, 101: 11, 102: 8, 103: 3, 104: 9, 105: 5, 106: 4, 107: 7, 108: 3,
        109: 6, 110: 3, 111: 5, 112: 4, 113: 5, 114: 6
    }

    sura_counts = {}
    for line in QuranCorpus.read_lines():
        sura, _, _ = line.split("|")
        sura = int(sura)
        sura_counts[sura] = sura_counts.get(sura, 0) + 1

    for sura, count in sura_counts.items():
        assert count == standard_verse_counts.get(
            sura), f"Sura {sura} has {count} verses, expected {standard_verse_counts.get(sura)}"
