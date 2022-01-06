__author__ = "Hassaan Abdul Razzaq <hassaan.maaldheefee@gmail.com>"

import re
import csv

ARAB_SET = u"\u0621-\u06FF"
THAA_SET = u"\u0780-\u07B1"
LONG_FILI = u"\u07A7\u07A9\u07AB\u07AD\u07AF"

INPUT_FILE = "utils/transliteration_test/arabic_words_with_next.txt"
OUTPUT_FILE = "utils/transliteration_test/arabic_words_with_next_out.csv"

TRANSLIT_FILE = "utils/transliteration_data/_quran_freq_dv.csv"
NEXT_WORDS_FILE = "utils/transliteration_data/_dhivehi_next_words.csv"

tranliteration_dicts = []
with open(TRANSLIT_FILE, mode='r', encoding='utf-8-sig', newline='') as translit_file:
    tranliteration_dicts = list(
        csv.DictReader(translit_file, delimiter=','))
next_words = []
with open(NEXT_WORDS_FILE, mode='r', encoding='utf-8-sig', newline='') as next_words_file:
    next_words = list(
        csv.DictReader(next_words_file, delimiter=','))


word_beginnigns = [("ކަމ", ""),
                   ("ކުޅަ", ""),
                   ("^ތެރި", ""),
                   ("އަށ", 1),
                   ("އަކ", 1),
                   ("އެކެ", 1),
                   ("ތައް", ""),
                   ("^ން", ""),
                   ("ވެރ", ""),
                   ("^ވަންތަ", "")]  # 1 if the previous word's last fili and next word's first akuru to be removed

regex_removable_letters = []
regex_all = []
for a in word_beginnigns:
    regex_all.append(a[0])
    if a[1] == 1:
        regex_removable_letters.append(a[0])

regex_removable_letters = "|".join(regex_removable_letters)
regex_all = "|".join(regex_all)


def separete_arabic_and_thaana(text):
    '''Takes a string with Arabic word(s) and the following Thaana word and separetes the Arabic from Thaana.

    Parameters
    ----------
    text : str
        String containing Arabic word followerd by the next thaana word.
        Eg: رحمن ވަންތަ

    Returns
    -------
    re.Match
        [1] = Arabic part, [2] = Thaana part
    '''

    result = re.search(
        f"([{ARAB_SET}][{ARAB_SET} ]+[{ARAB_SET}]?) ([{THAA_SET}]+)", text)
    return result


def get_first_word_data(text):
    global tranliteration_dicts
    return next((word for word in tranliteration_dicts if word['ar'] == text), None)


def get_next_word_data(text):
    global next_words
    return next((word for word in next_words if word['word'] == text), None)


def get_final_dhivehi(word_pair):
    first_word_data = get_first_word_data(word_pair[2])
    next_word_data = get_next_word_data(word_pair[1])

    joinable = bool(next_word_data["joinable"])
    trim_first_letter = bool(next_word_data["trim_first_letter"])
    unchangable = bool(first_word_data["unchangable"])

    if re.match(regex_removable_letters, word_pair[1]):
        trim_first_letter = True
    if re.match(regex_all, word_pair[1]):
        joinable = True

    # Mehun
    if (not unchangable) and trim_first_letter:
         # ބޭރު ބަސްބަހުގެ ތެރެއިން އަބަފިއްޔައް ނުވަތަ ދެމޭ ފިއްޔަކަށް ނިމޭ ބަސްތައް އެހެން ބަހަކާ ނުމެހޭނެއެވެ
        if word_pair[0][-1:] in (LONG_FILI + '\u07A6'):
            new_pair = word_pair
        else:
            new_pair = (word_pair[0][0:-1], word_pair[1][1:])
    else:
        new_pair = word_pair

    # Joining
    if trim_first_letter or joinable:
        # އަބަފިއްޔަށް ނިމޭ އަކުރެއްގެ ފަހަތައް ގަ ނުވަތަ ގެ އަންނަ ނަމަ އި އިތުރުކުރުން
        # މިސާލު: ޢިއްދައިގެ، ސަޖިދައިގައި
        if word_pair[0][-1:] == '\u07A6' and word_pair[1][0:1] == "ގ":
            new_pair = (new_pair[0] + 'އި', new_pair[1])

        # ކަލިމައިގެ ފަހަތަށް 'ގެ' ގުޅޭ އިރު ކުރީ އަކުރުގައި ސުކުން އޮތްނަމަ އުބުފިއްޔަށް ބަދަލު ކުރުން
        # މިސާލު: ރަޙްމަތްގެ، ޤުރްއާންގައި
        if word_pair[0][-1:] == '\u07B0' and word_pair[1][0:1] == "ގ":
            new_pair = (new_pair[0][0:-1] + '\u07AA', new_pair[1])
        
        return new_pair[0] + new_pair[1]
    else:
        return new_pair[0] + " " + new_pair[1]


def process_combo(row):
    '''Takes a string with Arabic word(s) and the following Thaana word and transliterated them to Thaana.

    Parameters
    ----------
    row : str
        String containing Arabic word followerd by the next thaana word.
        Eg: رحمن ވަންތަ

    Returns
    -------
    str
        Input string transliteraated th thaana.
        Eg: ރަޙްމާންވަންތަ
    '''

    sepatated = separete_arabic_and_thaana(row)
    processed_row = row

    try:
        first_word_data = get_first_word_data(sepatated[1])
        if first_word_data["dv"]:
            processed_row = get_final_dhivehi((
                first_word_data["dv"], sepatated[2], sepatated[1]))  # thaana, next_word, original
    except:
        pass

    # Final fixes
    processed_row = re.sub('\u07B0(.\u07B0)', "\u07AA\\1", processed_row)
    processed_row = re.sub('ﷲ އެއްވެސް', 'ﷲއެއްވެސް', processed_row)

    return processed_row


def main():
    '''Run this to test the script on INPUT_FILE to generate OUTPUT_FILE'''
    input_strings = []
    output_strings = []

    with open(INPUT_FILE, mode='r', encoding='utf-8', newline='') as txt_file:
        input_strings = list(map(str.strip, txt_file.readlines()))
        for row in input_strings:
            output_strings.append(process_combo(row))

    with open(OUTPUT_FILE, mode='w', encoding='utf-8-sig', newline='') as output_csv_file:
        writer = csv.writer(output_csv_file)
        writer.writerows(zip(input_strings, output_strings))


if __name__ == "__main__":
    # print(process_combo("سجدة ގައި"))
    # print(get_final_dhivehi(("ޤުރްއާން", "ގައި", "قرآن")))
    main()

