import re
from . import QuranCorpus


def test_no_bom():
    """
    Translation file should not contain BOM's
    as per Tanzil directive
    """
    trans = QuranCorpus.read_all()
    assert "\uFEFF" not in trans


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
