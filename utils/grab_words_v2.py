#!/usr/bin/env python -v
# -*- coding: utf-8 -*-

import re
import os
import collections

TRANS_FILE = "master_dv.divehi.txt"
WORD_LIST = "arabic_freq.txt"

ARAB_SET = u"\u0621-\u06FF"
THAA_SET = u"\u0780-\u07B1"

LONG_FILI = []

# match = re.findall(f"(?<!\w)[{ARAB_SET}][{ARAB_SET} ]+[{THAA_SET}]+",line)
# match = re.findall(f"(?<=[{ARAB_SET}]) [{THAA_SET}]+", line)

def get_arabic_word_list(in_file, remove_duplicates=False):
    arab_words = []
    for line in in_file:
        match = re.findall(f"[{ARAB_SET}][{ARAB_SET} ]+[{ARAB_SET}]?", line)
        if match:
            for m in match:
                m = m.strip()
                if remove_duplicates:
                    if not m in arab_words:
                        arab_words.append(m)
                else:
                    arab_words.append(m)
    return arab_words

def arabic_word_frequency(in_file):
    arab_words = get_arabic_word_list(in_file)
    return collections.Counter(arab_words)

def main():
    in_file = open(TRANS_FILE, "r", encoding="utf-8")

    try:
        os.remove(WORD_LIST)
    except:
        pass

    freq_list = arabic_word_frequency(in_file).most_common()

    with open(WORD_LIST, "w", encoding="utf-8") as out_file:
        for word in freq_list:
            out_file.write('%s\n' % ','.join(str(n) for n in word))


if __name__ == "__main__":
    main()
