import pygame
import sys

from game_class import QDutch

# --- Initialization ---
pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 60, 90
CARD_SPACING = 20
BG_COLOR = (34, 139, 34)      # Green table
BG_CARD_COLOR = (34, 100, 34)  # Light green for cards
CARD_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)

# --- Pygame Setup ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top View Table Game")
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

# --- Global Buttons ---
card_buttons = []
center_buttons = []


# --- Drawing Functions ---
def draw_card(x, y, text, rotation, player, card_index):
    # Create a transparent card surface
    card_surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
    card_surf.fill(CARD_COLOR)
    pygame.draw.rect(card_surf, TEXT_COLOR, card_surf.get_rect(), 2)

    # Render text onto the card surface
    if text:
        label = font.render(text, True, TEXT_COLOR)
        label_rect = label.get_rect(center=(CARD_WIDTH // 2, CARD_HEIGHT // 2))
        card_surf.blit(label, label_rect)

    # Rotate entire surface (card + text)
    rotated_surf = pygame.transform.rotate(card_surf, rotation)
    rect = rotated_surf.get_rect(center=(x, y))

    # Draw to main screen
    screen.blit(rotated_surf, rect.topleft)

    # Store clickable area
    card_buttons.append((rect, player, card_index))


def draw_table_with_states(players, show_states):
    screen.fill(BG_COLOR)
    card_buttons.clear()

    def get_card_text(index, card_index):
        if show_states and card_index < 2:
            return str(players[index].hand[card_index].measure_all())
        return ""

    # Player 1
    for i in range(4):
        x = WIDTH // 2 - 1.5 * (CARD_WIDTH + CARD_SPACING) + i * (CARD_WIDTH + CARD_SPACING)
        y = HEIGHT - CARD_HEIGHT - 40
        draw_card(x, y, get_card_text(0, i), 0, 0, i)

    # Player 3
    for i in range(4):
        x = WIDTH // 2 + 1.5 * (CARD_WIDTH + CARD_SPACING) - i * (CARD_WIDTH + CARD_SPACING)
        y = 40 + CARD_HEIGHT // 2
        draw_card(x, y, get_card_text(1, i), 180, 2, i)

    # Player 2
    for i in range(4):
        x = 40 + CARD_HEIGHT // 2
        y = HEIGHT // 2 - 1.5 * (CARD_WIDTH + CARD_SPACING) + i * (CARD_WIDTH + CARD_SPACING)
        draw_card(x, y, get_card_text(2, i), 90, 1, i)

    # Player 4
    for i in range(4):
        x = WIDTH - 40 - CARD_HEIGHT // 2
        y = HEIGHT // 2 + 1.5 * (CARD_WIDTH + CARD_SPACING) - i * (CARD_WIDTH + CARD_SPACING)
        draw_card(x, y, get_card_text(3, i), 270, 3, i)

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
        0: (WIDTH // 2, HEIGHT - 50),              # Bottom
        1: (175, HEIGHT // 2 - 25),                      # Left
        2: (WIDTH // 2, 20),                       # Top
        3: (WIDTH - 125, HEIGHT // 2 - 25),              # Right
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
            elif target_player == 1:  # Top
                x = WIDTH // 2 + 1.5 * (CARD_WIDTH + CARD_SPACING) - target_card_index * (CARD_WIDTH + CARD_SPACING)
                y = 40 + CARD_HEIGHT // 2
            elif target_player == 2:  # Left
                x = 40 + CARD_HEIGHT // 2
                y = HEIGHT // 2 - 1.5 * (CARD_WIDTH + CARD_SPACING) + target_card_index * (CARD_WIDTH + CARD_SPACING)
            elif target_player == 3:  # Right
                x = WIDTH - 40 - CARD_HEIGHT // 2
                y = HEIGHT // 2 + 1.5 * (CARD_WIDTH + CARD_SPACING) - target_card_index * (CARD_WIDTH + CARD_SPACING)

            # Draw the state value above the card
            label = font.render(str(measured_card_value), True, (255, 0, 0))  # Red for clarity
            screen.blit(label, label.get_rect(center=(x, y - CARD_HEIGHT // 2 - 10)))

            pygame.display.flip()

            # Block input until Enter or click
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    measured_card_displayed = False
                    measured_card_value = None
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
                                print("Deck clicked")
                                print(f"Card 1: {card1}, Card 2: {card2}")
                                drew_from_deck = True

                            elif drew_from_deck and not selected_card:
                                if label == "card 1":
                                    print("Card 1 clicked")
                                    selected_card = card1
                                elif label == "card 2":
                                    print("Card 2 clicked")
                                    selected_card = card2
                                can_click_player_cards = True

                    # --- Player card clicks ---
                    if can_click_player_cards:
                        for rect, player, card_index in card_buttons:
                            if rect.collidepoint((mx, my)):
                                print(f"Player {player + 1} clicked card {card_index + 1}")
                                
                                if selected_card.type == "Measurement":
                                    measured_card_value = players[player].hand[card_index].measure(selected_card.data)
                                    measured_target = (player, card_index)
                                    measured_card_displayed = True
                                    pending_player_done = True
                                    can_click_player_cards = False
                                    break

                                elif selected_card.type == "Operator":
                                    player_done = True
                                    break

                                elif selected_card.type == "State":
                                    if player == player_no:
                                        player_done = True
                                        break
                                    else:
                                        print("Cannot apply state card to another player.")
                                        continue

        # --- End-of-turn update ---
        if player_done:
            player_no = (player_no + 1) % 4
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
