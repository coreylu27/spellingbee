import generate_letters
import words as w

print("Welcome to Spelling Bee \nStandby ... Generating Game")

game_letters, center_letter = generate_letters.find_one_valid_game(200)

game_loop = True

points = 0
used_words = []



print(f"The Game Letters are: {''.join(game_letters)} \nThe Center Letter is: {center_letter}")
# print(generate_letters.printWords(game_letters, center_letter))

while game_loop:
    guess = input("Guess a word: ").lower()

    if guess == "/quit":
        game_loop = False
        continue

    if guess in used_words:
        print("Already Guessed")
        continue
    if len(guess) < 4:
        print("Not enough letters")
        continue

    guess_points, pangram = w.getScore(guess, game_letters, center_letter)
    points += guess_points

    if guess_points == 0:
        print("Not a valid word")
        continue

    if pangram:
        print(f"PANGRAM! {guess}: {guess_points}")
    else:
        print(f"{guess}: {guess_points}")

    print(f"Total Score: {points}")
