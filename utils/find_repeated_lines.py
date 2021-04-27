import re

TRANS_FILE = "master_dv.divehi.txt"
WORD_LIST = "repeated_lines.txt"

def main():
    with open(TRANS_FILE, "r", encoding="utf-8") as in_file:
        trans = in_file.read()

    found = re.finditer(r"\d+\|\d+\|(.+)(\n\d+\|\d+\|\1)+", trans)

    with open(WORD_LIST, "w", encoding="utf-8") as out_file:
        trans = out_file
        for line in found:
            out_file.writelines(line.group(0) + '\n')


if __name__ == "__main__":
    main()
