#!/bin/python
# -*- coding: utf-8 -*- 

# this script will look into the word_map file
# and replace all occurances of arabic text 
# output to gen_alt

# TODO: get off your lazy ass and writeup a proper
# replacement without having to rely on human interaction

import csv, codecs, cStringIO, os


TRANS_FILE = "../master_dv.divehi.txt"
ALT_TRANS  = "../alt_(autoGen)dv.divehi.txt"
MAP_FILE   = "../word_map.csv"


def main():
	map_file = codecs.open(MAP_FILE,encoding='utf-8')
	master_file = codecs.open(TRANS_FILE,encoding="utf-8")

	#delete the file first
	try:
		os.remove(ALT_TRANS)
	except:
		pass

	alt_file = codecs.open(ALT_TRANS,"wb",encoding="utf-8")

	# watch out for those newlines
	map_dict = dict([row.split('\t',1) for row in map_file])
	
	for line in master_file:
		replaced = line

		# horribly inefficient I know
		for key in map_dict.keys():
				replaced = replaced.replace(key.strip(),map_dict[key].strip())

		alt_file.write(replaced)


	alt_file.close()

if __name__ == '__main__':
	main()