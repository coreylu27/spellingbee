import json
import string
import random
import words as w

letters = list(string.ascii_lowercase)

word_list = w.words_list

def checkValidGame(game_letters: set, center_letter: str) -> bool:
    max_score, pangram = getMaxScore(game_letters, center_letter)
    return max_score >= minimum_points and pangram

def get_one_game():
    while True:
        center_letter, game = generate_random_game()
        if checkValidGame(game, center_letter):
            return game, center_letter

def generate_random_game():
    game = set(random.choices(letters, k=7))
    center_letter = random.choice(list(game))
    return center_letter, game

def getMaxScore(game_letters: set, center_letter: str):
    score = 0
    pangram_found = False
    for word in word_list:
        word_score, is_pangram = w.getScore(word, game_letters, center_letter)
        score += word_score
        if is_pangram:
            pangram_found = True
    return score, pangram_found

def printWords(game_letters: set, center_letter: str):
    valid_words = []
    for word in word_list:
        score, _ = w.getScore(word, game_letters, center_letter)
        if score > 0:
            valid_words.append((word, score))

    sorted_words = sorted(valid_words, key=lambda x: x[1], reverse=True)
    for word, score in sorted_words:
        print(f"Word: {word} Score: {score}")
        print("Pangram: " + str(w.isPangram(word, game_letters)))

def find_one_valid_game(points):
    global minimum_points
    minimum_points = points

    game_letters, center_letter = get_one_game()
    print(f"Game letters: {''.join(game_letters)}, Center letter: {center_letter}")
    max_score, _ = getMaxScore(game_letters, center_letter)
    print(f"Max score: {max_score}")
    printWords(game_letters, center_letter)

find_one_valid_game(400)
