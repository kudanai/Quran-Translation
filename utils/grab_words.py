#!/usr/bin/env python -v
# -*- coding: utf-8 -*-

import re,codecs,os

TRANS_FILE = "../master_dv.divehi.txt"
WORD_LIST = "../arabic_words.txt"

# a charset of all arabic characters inserted here
# u0600 - u06FF is the basic arabic range

ARAB_SET = u"\u0600-\u06FF"


def main():
	
	master_file = codecs.open(TRANS_FILE,"rb",encoding="utf-8")

	try:
		os.remove(WORD_LIST)
	except:
		pass
 

	arab_words = []

	for line in master_file:
		match = re.findall(u"[%s]+" % ARAB_SET,line)
		if match:
			for m in match:
				if not m in arab_words:
					arab_words.append(m)


	word_file   = codecs.open(WORD_LIST,"wb",encoding="utf-8")
	word_file.write('\n'.join(arab_words))
	word_file.close()

if __name__ == "__main__":
	main()
