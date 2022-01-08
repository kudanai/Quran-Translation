__author__ = "Hassaan Abdul Razzaq <hassaan.maaldheefee@gmail.com>"

import re
import csv
import transliterate_arabic_to_thaana as trans

INPUT_FILE = "master_dv.divehi.txt"
OUTPUT_FILE = "alt_dv.divehi.txt"


def main():
    find_combos = re.compile(
        f"(?<!\w)[{trans.ARAB_SET}][{trans.ARAB_SET} ]+[{trans.THAA_SET}]+")
    with open(INPUT_FILE, mode='r', encoding='utf-8', newline='') as txt_file, open(OUTPUT_FILE, mode='w', encoding='utf-8', newline='') as out_file:
        for row in txt_file.readlines():
            a = find_combos.finditer(row)
            for b in a:
                find_text = b[0]
                change_text = trans.process_combo(b[0])
                row = re.sub(find_text, change_text, row, count=1)
            for single_word in re.finditer(f"(?<!\w)[{trans.ARAB_SET}]+", row):
                translit_word = trans.get_first_word_data(single_word[0])
                if translit_word:
                    row = re.sub(single_word[0], translit_word["dv"]
                                 if translit_word["dv"] else single_word[0], row)
            out_file.writelines(row)


if __name__ == "__main__":
    main()
