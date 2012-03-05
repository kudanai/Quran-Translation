#!/usr/bin/env python -v
# -*- coding: utf-8 -*-

import re

def main():
    
    THAANA_FILI = u"\u07A6\u07AC\u07A8\u07AE\u07AA\u07A7\u07AD\u07A9\u07AF\u07AB"
 
 	# check for repeated instances of fili without an akuru
 	# there seem to be a few of these around.
 	
    with open("dv.divehi.txt","rb") as spam:
        for line in spam:
            if re.findall(u"[%s]{2}" % THAANA_FILI,line):
                surah,ayat,text=line.split("|")
                print surah,ayat


if __name__ == "__main__":
	main()
