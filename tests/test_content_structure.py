from . import QuranCorpus


def test_line_count():
    """
    Number of lines in translation files must == 6236
    """
    lines = list(QuranCorpus.read_lines())
    assert len(lines) == 6236, f"Expected 6236 lines, got {len(lines)}"
