import pandas


def generate_phonetic():
    word = input("Please input a word to convert: ").upper()
    try:
        word_in_nato_codes = [nato_letters_codes[letter] for letter in word if letter != " "]
    except KeyError:
        print("Sorry, only letters of the alphabet please.")
        generate_phonetic()
    else:
        print(word_in_nato_codes)


nato_alphabet = pandas.read_csv("nato_phonetic_alphabet.csv")
nato_letters_codes = {row.letter: row.code for (index, row) in nato_alphabet.iterrows()}

generate_phonetic()
