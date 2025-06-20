import pygame
import sys
import os

from game_class import QDutch
from card_renderer import draw_card_front, draw_card_back

# --- Initialization ---
pygame.init()

# Get the directory where the running script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

SCREEN_SIZE = (900, 600)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Modular Card Renderer")

# Build the absolute path to the image file
bg_image_path = os.path.join(SCRIPT_DIR, "assets/background.png")
bg_image = pygame.image.load(bg_image_path).convert_alpha()

measurement_img_path = os.path.join(SCRIPT_DIR, "assets/measure.png")
measurement_img = pygame.image.load(measurement_img_path).convert_alpha()

# --- Constants ---
WIDTH, HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 60, 90
CARD_SPACING = 20
font = pygame.font.SysFont("arial", 100, bold=False)

# Colors
BG_COLOR = (34, 139, 34)      # Green table
BG_CARD_COLOR = (34, 100, 34)  # Light green for cards
CARD_COLOR = (255, 255, 255)
TEXT_COLOR = (20, 20, 20)
COLOR_TOP = pygame.Color(250, 128, 114)
COLOR_BOTTOM = pygame.Color(255, 224, 230)
HIDDEN_BASE = (180, 180, 180)

# --- Pygame Setup ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top View Table Game")
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

# --- Global Buttons ---
card_buttons = []
center_buttons = []


def draw_table_with_states(players, show_states):
    screen.fill(BG_COLOR)
    card_buttons.clear()

    # --- Player 1 (Bottom) ---
    for i in range(4):
        x = WIDTH // 2 - 1.5 * (CARD_WIDTH + CARD_SPACING) + i * (CARD_WIDTH + CARD_SPACING)
        y = HEIGHT - CARD_HEIGHT - 40
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        if show_states and i < 2:
            value = players[0].hand[i].measure_all()
            bits = list(f"{value:03b}")
            draw_card_front(screen, bits, (x, y), (CARD_WIDTH, CARD_HEIGHT), 0)
        else:
            draw_card_back(screen, bg_image, (x, y), (CARD_WIDTH, CARD_HEIGHT), 0)
        card_buttons.append((rect, 0, i))

    # --- Player 3 (Top) ---
    for i in range(4):
        x = WIDTH // 2 + 1.5 * (CARD_WIDTH + CARD_SPACING) - i * (CARD_WIDTH + CARD_SPACING)
        y = 40 + CARD_HEIGHT // 2
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        if show_states and i < 2:
            value = players[2].hand[i].measure_all()
            bits = list(f"{value:03b}")
            draw_card_front(screen, bits, (x, y), (CARD_WIDTH, CARD_HEIGHT), 180)
        else:
            draw_card_back(screen, bg_image, (x, y), (CARD_WIDTH, CARD_HEIGHT), 180)
        card_buttons.append((rect, 2, i))

    # --- Player 2 (Left) ---
    for i in range(4):
        x = 40 + CARD_HEIGHT // 2
        y = HEIGHT // 2 - 1.5 * (CARD_WIDTH + CARD_SPACING) + i * (CARD_WIDTH + CARD_SPACING)
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        if show_states and i < 2:
            value = players[1].hand[i].measure_all()
            bits = list(f"{value:03b}")
            draw_card_front(screen, bits, (x, y), (CARD_WIDTH, CARD_HEIGHT), 270)
        else:
            draw_card_back(screen, bg_image, (x, y), (CARD_WIDTH, CARD_HEIGHT), 270)
        card_buttons.append((rect, 1, i))

    # --- Player 4 (Right) ---
    for i in range(4):
        x = WIDTH - 60 - CARD_HEIGHT // 2
        y = HEIGHT // 2 + 1.5 * (CARD_WIDTH + CARD_SPACING) - i * (CARD_WIDTH + CARD_SPACING)
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        if show_states and i < 2:
            value = players[3].hand[i].measure_all()
            bits = list(f"{value:03b}")
            draw_card_front(screen, bits, (x, y), (CARD_WIDTH, CARD_HEIGHT), 90)
        else:
            draw_card_back(screen, bg_image, (x, y), (CARD_WIDTH, CARD_HEIGHT), 90)
        card_buttons.append((rect, 3, i))


def draw_center_elements():
    center_buttons.clear()

    center_x, center_y = WIDTH // 2, HEIGHT // 2

    # Dutch button
    dutch_rect = pygame.Rect(center_x - 160, center_y - 25, 100, 50)
    pygame.draw.rect(screen, (255, 125, 25), dutch_rect)
    dutch_text = font.render("Dutch", True, TEXT_COLOR)
    screen.blit(dutch_text, dutch_text.get_rect(center=dutch_rect.center))
    center_buttons.append((dutch_rect, "Dutch"))

    # Deck
    deck_rect = pygame.Rect(center_x - CARD_WIDTH // 2, center_y - CARD_HEIGHT // 2, CARD_WIDTH, CARD_HEIGHT)
    pygame.draw.rect(screen, (180, 180, 180), deck_rect)
    deck_text = font.render("Deck", True, TEXT_COLOR)
    screen.blit(deck_text, deck_text.get_rect(center=deck_rect.center))
    center_buttons.append((deck_rect, "deck"))

    # Cards (no text on these two)
    card1_rect = pygame.Rect(center_x + 70, center_y - CARD_HEIGHT // 2, CARD_WIDTH, CARD_HEIGHT)
    pygame.draw.rect(screen, BG_CARD_COLOR, card1_rect)
    center_buttons.append((card1_rect, "card 1"))

    card2_rect = pygame.Rect(center_x + 140, center_y - CARD_HEIGHT // 2, CARD_WIDTH, CARD_HEIGHT)
    pygame.draw.rect(screen, BG_CARD_COLOR, card2_rect)
    center_buttons.append((card2_rect, "card 2"))

def draw_player_labels(show_states, current_player_no):
    label_font = pygame.font.SysFont(None, 28)

    player_positions = {
        0: (WIDTH // 2 + 25, HEIGHT - 150),              # Bottom
        1: (225, HEIGHT // 2 + 25),                      # Left
        2: (WIDTH // 2 + 25, 200),                       # Top
        3: (WIDTH - 125, HEIGHT // 2 + 25),              # Right
    }

    for i in range(4):
        if show_states or i == current_player_no:
            label = label_font.render(f"Player {i + 1}", True, (255, 255, 255))
            pos = player_positions[i]

            # Center horizontally or vertically based on side
            if i == 0 or i == 2:  # Bottom or top
                label_rect = label.get_rect(center=pos)
            else:  # Left or right
                label_rect = label.get_rect(center=pos)
                label = pygame.transform.rotate(label, 270/i)

            screen.blit(label, label_rect)

def draw_start_message():
    msg_font = pygame.font.SysFont(None, 36)
    message = "Press Enter to Start"
    text = msg_font.render(message, True, (255, 255, 255))
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)

def show_ranking_screen(ranking, players):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Over - Rankings")
    clock = pygame.time.Clock()
    font_large = pygame.font.SysFont(None, 40)
    font_title = pygame.font.SysFont(None, 60)

    while True:
        screen.fill(BG_COLOR)

        # Title
        title = font_title.render("Final Rankings", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

        # Rankings (centered)
        for i, (name, score, position) in enumerate(ranking):
            name_cap = name.title()  # Capitalize each word
            label = font_large.render(f"{position}. {name_cap}   Score: {score}", True, (255, 255, 255))
            screen.blit(label, (WIDTH // 2 - label.get_width() // 2, 120 + i * 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)


# --- Main Game Loop ---
def main():
    game = QDutch()
    game.start_game()
    game.init_routine()
    players = game.players

    turn_no = 0
    player_no = 0
    show_states = True
    showed_initial_states = False
    dutch_call = False
    player_dutch = None
    dutch_turn = None
    drew_from_deck = False
    selected_card = None
    can_click_player_cards = False
    player_done = False
    measured_card_displayed = False
    measured_card_value = None
    measured_target = None
    pending_player_done = False
    card1_preview = None
    card2_preview = None

    while True:
        # --- Game end condition ---
        if dutch_turn is not None and turn_no == dutch_turn + 1 and player_no == player_dutch:
            game.end_routine()
            ranking = game.get_ranking()
            pygame.quit()
            show_ranking_screen(ranking, players)
            sys.exit()

        # --- Display measured card alone ---
        if measured_card_displayed:
            # Redraw the full table and card positions as usual
            draw_table_with_states(players, show_states=False)
            draw_player_labels(False, player_no)
            draw_center_elements()

            # Draw the measurement value only on the targeted card
            target_player = measured_target[0]
            target_card_index = measured_target[1]

            # Compute position based on player and index
            if target_player == 0:  # Bottom
                x = WIDTH // 2 - 1.5 * (CARD_WIDTH + CARD_SPACING) + target_card_index * (CARD_WIDTH + CARD_SPACING)
                y = HEIGHT - CARD_HEIGHT - 40
            elif target_player == 2:  # Top
                x = WIDTH // 2 + 1.5 * (CARD_WIDTH + CARD_SPACING) - target_card_index * (CARD_WIDTH + CARD_SPACING)
                y = 40 + CARD_HEIGHT // 2
            elif target_player == 1:  # Left
                x = 40 + CARD_HEIGHT // 2
                y = HEIGHT // 2 - 1.5 * (CARD_WIDTH + CARD_SPACING) + target_card_index * (CARD_WIDTH + CARD_SPACING)
            elif target_player == 3:  # Right
                x = WIDTH - 40 - CARD_HEIGHT // 2
                y = HEIGHT // 2 + 1.5 * (CARD_WIDTH + CARD_SPACING) - target_card_index * (CARD_WIDTH + CARD_SPACING)

            # Draw the state value above the card
            value_int = game.apply_operator_card(target_player, target_card_index, selected_card)
            bits = [None, None, None]
            bits[selected_card.data] = value_int
            draw_card_front(screen, bits, (x, y), (CARD_WIDTH, CARD_HEIGHT),  0)

            pygame.display.flip()

            # Block input until Enter or click
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    measured_card_displayed = False
                    measured_target = None
                    if pending_player_done:
                        player_done = True
                        pending_player_done = False
            continue


        # --- Normal game drawing ---
        draw_table_with_states(players, show_states)
        if not show_states:
            draw_center_elements()
        else:
            draw_start_message()
        
        if drew_from_deck and not selected_card and card1_preview and card2_preview:
            # Coordinates for temporary card preview
            x1 = WIDTH // 2 - CARD_WIDTH - 10
            x2 = WIDTH // 2 + 10
            y = HEIGHT // 2 - CARD_HEIGHT // 2
            bits1 = card1_preview.data
            bits2 = card2_preview.data
            if card1_preview.type == "State":
                bits1 = list(f"{bits1:03b}")
            if card2_preview.type == "State":
                bits2 = list(f"{bits2:03b}")
            draw_card_front(screen, bits1, (x1+135, y), (CARD_WIDTH, CARD_HEIGHT), 0, card_type=card1_preview.type)
            draw_card_front(screen, bits2, (x2+135, y), (CARD_WIDTH, CARD_HEIGHT), 0, card_type=card2_preview.type)

        draw_player_labels(show_states, player_no)

        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not showed_initial_states:
                    show_states = False
                    showed_initial_states = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not show_states:
                    mx, my = pygame.mouse.get_pos()

                    # --- Center interactions ---
                    for rect, label in center_buttons:
                        if rect.collidepoint((mx, my)):

                            if not drew_from_deck and not dutch_call:
                                if label == "Dutch":
                                    game.call_dutch()
                                    print("Dutch called")
                                    dutch_call = True
                                    player_dutch = player_no
                                    dutch_turn = turn_no
                                    player_done = True
                                    break

                            if not drew_from_deck and label == "deck":
                                card1, card2 = game.draw_cards()
                                card1_preview = card1
                                card2_preview = card2
                                drew_from_deck = True
                                print(f"Card 1: {card1}, Card 2: {card2}")

                            elif drew_from_deck and not selected_card:
                                if label == "card 1":
                                    selected_card = card1
                                    card1_preview = None
                                    card2_preview = None
                                    print("Card 1 clicked")
                                elif label == "card 2":
                                    selected_card = card2
                                    card1_preview = None
                                    card2_preview = None
                                    print("Card 2 clicked")
                            can_click_player_cards = True

                    # --- Player card clicks ---
                    if can_click_player_cards:
                        for rect, player, card_index in card_buttons:
                            if rect.collidepoint((mx, my)):
                                print(f"Player {player + 1} clicked card {card_index + 1}")
                                
                                if selected_card.type == "Measurement":
                                    measured_card_value = game.apply_operator_card(player, card_index, selected_card)
                                    measured_target = (player, card_index)
                                    measured_card_displayed = True
                                    pending_player_done = True
                                    can_click_player_cards = False
                                    break
                                elif selected_card.type == "Operator":
                                    game.apply_operator_card(player, card_index, selected_card)
                                    player_done = True
                                    break

                                elif selected_card.type == "State":
                                    if player == player_no:
                                        game.apply_state_card(card_index, selected_card)
                                        player_done = True
                                        break
                                    else:
                                        print("Cannot apply state card to another player.")
                                        continue

        # --- End-of-turn update ---
        if player_done:
            player_no = (player_no + 1) % 4
            game.next_player()
            if player_no == 0:
                turn_no += 1

            drew_from_deck = False
            selected_card = None
            can_click_player_cards = False
            player_done = False

        pygame.display.flip()
        clock.tick(60)



# --- Entry Point ---
if __name__ == "__main__":
    main()
