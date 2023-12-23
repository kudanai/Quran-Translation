from pathlib import Path


class QuranCorpus:
    """
    Simple wrapper class to read
    content from master_dv.divehi.txt
    """

    BASE_PATH = Path(__file__).resolve().parent.parent
    TRANSLATION_FILE = BASE_PATH / "master_dv.divehi.txt"

    @staticmethod
    def read_all():
        with open(QuranCorpus.TRANSLATION_FILE, "r") as f:
            return f.read()

    @staticmethod
    def read_lines():
        with open(QuranCorpus.TRANSLATION_FILE, "r") as f:
            for line in f:
                if line.startswith("\n") or line.startswith("#"):
                    continue

                yield line
