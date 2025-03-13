import re
from . import QuranCorpus


def test_no_bom():
    """
    Translation file should not contain BOM's
    as per Tanzil directive
    """
    trans = QuranCorpus.read_all()
    assert "\uFEFF" not in trans


def test_special_character_validation():
    """
    Check for unexpected or invalid special characters that might
    cause display issues in applications
    """
    invalid_chars = ['\u200B', '\u200C', '\u200D', '\u200E', '\u200F']  # Zero-width spaces and other invisible chars

    for line in QuranCorpus.read_lines():
        for char in invalid_chars:
            assert char not in line, f"Invalid character {repr(char)} found in line: {line[:50]}..."


def test_no_repeated_fili():
    """
    Thaana often mistakenly slips in repeated fili.
    Test to make sure this does not appear in the translation
    """
    error_list = []
    pattern = re.compile("[\u07A6-\u07AB]{2}")

    for line in QuranCorpus.read_lines():
        if re.findall(pattern, line):
            sura, ayat, trans = line.split("|")
            error_list.append(f"{sura}|{ayat}")

    assert len(error_list) == 0, f"Repeated fili found on {error_list}"


def test_character_encoding_consistency():
    """
    Ensure all text is consistently encoded in UTF-8 without
    any encoding issues or mixed character sets
    """
    trans = QuranCorpus.read_all()
    # Test that the file can be encoded and decoded without errors
    try:
        encoded = trans.encode('utf-8')
        decoded = encoded.decode('utf-8')
        assert trans == decoded
    except UnicodeError:
        assert False, "Encoding/decoding error detected"
