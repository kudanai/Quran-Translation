from . import TRANSLATION_FILE


def test_line_count():
    """
    Number of lines in translation files must == 6236
    """
    with open(TRANSLATION_FILE, "r") as f:
        lines = [line for line in f.readlines() if not line.startswith("#")]
        assert len(lines) == 6236, f"Expected 6236 lines, got {len(lines)}"
