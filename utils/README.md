# Utilities

These utility scripts will perform various automated tasks on the translation. Please make sure you don't really change the master_txt translation file.

functions of these utils are as follows

## gen_alternate.py

the script looks into the word_map.csv (tab separated) file for a mapping of arabic->dhivehi words and replaces them in the translation file accordingly to generate the alt_autogen translation file.

## tanzil_import.py

will download the latest translation files available on tanzil.net and add them to an sqlite3 database.

## transError_check.py

various automated routines for checking common errors in the translation. currently only checks for repeated "fili" without a consonant.

## navigator.py

**incomplete** a simple quran navigator which might help editors review the translation files.