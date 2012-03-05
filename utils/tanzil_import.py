#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# this file is part of the Dhivehi Quran translation
# maintainance project

__author__ = "KudaNai <kudanai@gmail.com>"


import sqlite3
import codecs
import urllib

TRANS_FILE = "dv.divehi.txt"
DB_FILE = "quranmv.sqlite3"

def main():
    
    # -- download the latest version from tanzil.net
    try:
        print "downloading translation from tanzil.net"
        urllib.urlretrieve ("http://tanzil.net/trans/dv.divehi",TRANS_FILE)
    except:
        print "error downloading from tanzil. quitting"

    # -- yes we could have read the file directly from urllib
    # -- but we're taking the long way around since we're dealing with thaana here
    fReader = codecs.open(TRANS_FILE,encoding="utf-8")

    # -- import the translation into the database.
    # -- this is for private use only.. do main edits in text
    
    print "importing to the database"
    
    with sqlite3.connect(DB_FILE) as dbConn:
        dbCurr = dbConn.cursor()
        
        # -- drop existing tables and create a new one		
        dbCurr.execute('DROP TABLE IF EXISTS translation')
        dbCurr.execute('CREATE TABLE translation("index" INTEGER PRIMARY KEY,surah INTEGER,ayat INTEGER,"text" TEXT)')
            
        for line in fReader:
          if line.startswith("\n") or line.startswith("#"):
          	continue
          stuff=line.split("|")
          dbCurr.execute("INSERT INTO translation('surah','ayat','text') VALUES (?,?,?)",stuff)
          
        dbCurr.execute('SELECT COUNT(*) FROM translation')
        print "%d records inserted" % dbCurr.fetchone()
        
    fReader.close()

if __name__ == "__main__":
	main()