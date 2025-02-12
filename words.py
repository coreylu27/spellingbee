import json
import string

with open('dictionary.json') as json_file:
    words_list = set(json.load(json_file).keys())  # Ensure words are a set for faster lookup

letters = list(string.ascii_lowercase)

def isPangram(word: str, game_letters: set) -> bool:
    word_letters = set(word)
    return word_letters == game_letters

def getScore(word: str, letters: set, center_letter: str):
    pangram = isPangram(word, letters)
    word_letters = set(word)
    if (
        word in words_list and
        center_letter in word and
        len(word) >= 4 and
        word_letters.issubset(letters)
    ):
        score = 1 if len(word) == 4 else len(word)

        if pangram:
            score += 7

        return score, pangram
    return 0, False