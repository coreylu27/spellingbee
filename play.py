import pygame
import generate_letters
import words as w
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_MODE_BG = (30, 30, 30)
DARK_MODE_TEXT = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
LIGHT_GREY = (211, 211, 211)
DARK_GREY = (169, 169, 169)
ORANGE = (255, 165, 0)

# Fonts
FONT = pygame.font.Font(None, 30)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spelling Bee")

print("Welcome to Spelling Bee \nStandby ... Generating Game")

# Generate game letters
# while True:
#     game_letters, center_letter = generate_letters.find_one_valid_game(200)
#     game_letters = list(game_letters)  # Ensure game_letters is a list
#     if len(game_letters) == 7:
#         break
#     print(f"Generated letters: {game_letters}, Center letter: {center_letter}")

# game_letters, center_letter = generate_letters.find_one_valid_game(200)
#
# game_letters = list(game_letters)

game_letters = ['t', 'a', 's', 'l', 'b', 'c', 'i']
center_letter = 'l'

points = 0
used_words = []
input_text = ""
message = ""
dark_mode = False

print(f"The Game Letters are: {''.join(game_letters)} \nThe Center Letter is: {center_letter}")
generate_letters.printWords(game_letters, center_letter)


def draw_hexagon(surface, color, position, size):
    angle = 60
    points = []
    for i in range(6):
        theta = math.radians(angle * i)
        x = position[0] + size * math.cos(theta)
        y = position[1] + size * math.sin(theta)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points)

def draw_hexagon_button(text, x, y, size, color, text_color):
    draw_hexagon(screen, color, (x, y), size)
    button_text = FONT.render(text, True, text_color)
    screen.blit(button_text, (x - button_text.get_width() // 2, y - button_text.get_height() // 2))

def draw_hexagon_buttons(letters, center_letter, x, y, size, color, text_color):
    positions = [
        (x, y - size * 1.5),  # Top
        (x + size * 1.3, y - size * 0.75),  # Top-right
        (x + size * 1.3, y + size * 0.75),  # Bottom-right
        (x, y + size * 1.5),  # Bottom
        (x - size * 1.3, y + size * 0.75),  # Bottom-left
        (x - size * 1.3, y - size * 0.75)  # Top-left
    ]
    for i, pos in enumerate(positions):
        draw_hexagon_button(letters[i], pos[0], pos[1], size, color, text_color)
    draw_hexagon_button(center_letter, x, y, size, ORANGE, WHITE)

def draw_button(text, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)
    button_text = FONT.render(text, True, text_color)
    screen.blit(button_text, (x + (width - button_text.get_width()) // 2, y + (height - button_text.get_height()) // 2))

def draw_wrapped_text(text, x, y, width, font, color):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        if font.size(test_line)[0] <= width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)

    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (x, y + i * font.get_height()))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                guess = input_text.lower()
                if guess == "/quit":
                    running = False
                elif guess in used_words:
                    message = "Already Guessed"
                elif len(guess) < 4:
                    message = "Not enough letters"
                elif center_letter not in guess:
                    message = "Not containing center letter"
                else:
                    try:
                        if not w.is_valid_word(guess, game_letters, center_letter):
                            message = "Not a word"
                        else:
                            guess_points, pangram = w.getScore(guess, game_letters, center_letter)
                            points += guess_points
                            used_words.append(guess)
                            message = ""
                    except Exception as e:
                        message = f"Error: {str(e)}"
                        print(f"Error checking word validity: {e}")
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for i, letter in enumerate(game_letters):
                if 20 + i * 50 <= mouse_x <= 70 + i * 50 and 300 <= mouse_y <= 350:
                    input_text += letter
            # Check if the dark mode button is clicked
            if 700 <= mouse_x <= 820 and 20 <= mouse_y <= 60:
                dark_mode = not dark_mode

    # Clear the screen
    if dark_mode:
        screen.fill(DARK_MODE_BG)
        text_color = DARK_MODE_TEXT
    else:
        screen.fill(LIGHT_GREY)
        text_color = BLACK

    # Render input text area
    pygame.draw.rect(screen, WHITE if not dark_mode else DARK_MODE_TEXT, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 200, 300, 40), border_radius=10)
    input_text_surface = FONT.render(input_text, True, text_color)
    screen.blit(input_text_surface, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 190))

    # Render game letters as hexagon buttons
    draw_hexagon_buttons(game_letters, center_letter, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, 50, LIGHT_BLUE if not dark_mode else DARK_GREY, BLACK if not dark_mode else WHITE)

    # Render game letters
    letters_text = FONT.render(f"Game Letters: {''.join(game_letters)}", True, text_color)
    center_letter_text = FONT.render(f"Center Letter: {center_letter}", True, text_color)
    screen.blit(letters_text, (20, 20))
    screen.blit(center_letter_text, (20, 60))

    # Render points
    points_text = FONT.render(f"Points: {points}", True, text_color)
    screen.blit(points_text, (20, 140))

    # Render used words
    used_words_text = f"Used Words: {', '.join(used_words)}"
    draw_wrapped_text(used_words_text, 20, 180, 760, FONT, text_color)

    # Render message
    message_text = FONT.render(message, True, RED)
    screen.blit(message_text, (20, 220))

    # Render dark mode button
    draw_button("Dark Mode", 600, 20, 120, 40, DARK_GREY, WHITE)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.display.quit()
pygame.font.quit()
pygame.quit()