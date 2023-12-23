# Utilities

These utility scripts will perform various automated tasks on the translation. Please make sure you don't really change the master_txt translation file.

functions of these utils are as follows

## grab_words.py

parses through the main translation file and attempts to retreive the arabic words that are in there, and spits them out to arabic_words.txt in the root folder. It was meant to be used only once, to help create the word_map used by gen_alternate.py

## gen_alternate.py

the script looks into the word_map.csv (tab separated) file for a mapping of arabic->dhivehi words and replaces them in the translation file accordingly to generate the alt_autogen translation file.

## tanzil_import.py

will download the latest translation files available on tanzil.net and add them to an sqlite3 database.

## transError_check.py

various automated routines for checking common errors in the translation. currently only checks for repeated "fili" without a consonant.