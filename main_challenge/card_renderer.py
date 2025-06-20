import pygame
import sys
import os

pygame.init()

# Get the directory where the running script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Build the absolute path to the image file
bg_image_path = os.path.join(SCRIPT_DIR, "background.png")

SCREEN_SIZE = (900, 600)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Modular Card Renderer")
bg_image = pygame.image.load("background.png").convert_alpha()

# Colors
BG = (0, 0, 0)
CARD_COLOR = (255, 255, 255)
TEXT_COLOR = (20, 20, 20)
COLOR_TOP = pygame.Color(250, 128, 114)
COLOR_BOTTOM = pygame.Color(255, 224, 230)
HIDDEN_BASE = (180, 180, 180)

font = pygame.font.SysFont("arial", 100, bold=False)

def lerp_color(c1, c2, t):
    return pygame.Color(
        int(c1.r + (c2.r - c1.r) * t),
        int(c1.g + (c2.g - c1.g) * t),
        int(c1.b + (c2.b - c1.b) * t)
    )

def draw_blur_circle(surface, center, radius):
    x, y = center
    pygame.draw.circle(surface, HIDDEN_BASE, (x, y), radius)
    blur_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for i in range(5, 0, -1):
        alpha = 30 + i * 15
        r = int(radius * i / 5)
        color = (255, 255, 255, alpha)
        pygame.draw.circle(blur_surface, color, (radius, radius), r)
    surface.blit(blur_surface, (x - radius, y - radius))

def draw_card(board_surface, bits, position, size, rotation=0):
    """
    Draws a card at a given position with rotation.
    - board_surface: main surface to draw onto
    - bits: list of 3 values (0, 1, or None)
    - position: (x, y) top-left position on the board
    - size: (width, height) of the card
    - rotation: angle in degrees (clockwise)
    """
    width, height = size
    card_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(card_surface, CARD_COLOR, card_surface.get_rect().inflate(-20, -20), border_radius=20)

    n = len(bits)
    circle_radius = int(min(width, height) * 0.15)

    # Scaled margins based on height
    top_margin = int(height * 0.18)
    bottom_margin = int(height * 0.18)

    total_height = height - top_margin - bottom_margin
    spacing = total_height / (n - 1 if n > 1 else 1)

    for i, bit in enumerate(bits):
        y = top_margin + i * spacing
        x = width // 2
        t = i / (n - 1) if n > 1 else 0

        if bit is None:
            draw_blur_circle(card_surface, (x, int(y)), circle_radius)
        else:
            circle_color = lerp_color(COLOR_TOP, COLOR_BOTTOM, t)
            pygame.draw.circle(card_surface, circle_color, (x, int(y)), circle_radius)

            scale_font = pygame.font.SysFont("arial", int(circle_radius * 1.5), bold=False)
            txt = scale_font.render(str(bit), True, TEXT_COLOR)
            txt_rect = txt.get_rect(center=(x, int(y)))
            card_surface.blit(txt, txt_rect)

    # Rotate and blit
    rotated_surface = pygame.transform.rotate(card_surface, rotation)
    rotated_rect = rotated_surface.get_rect(center=(position[0] + width // 2, position[1] + height // 2))
    board_surface.blit(rotated_surface, rotated_rect.topleft)

def draw_card_back(board_surface, bg_image, position, size, rotation=0):
    width, height = size
    # Scale and rotate the already loaded image
    scaled_img = pygame.transform.smoothscale(bg_image, (width, height))
    rotated_bg = pygame.transform.rotate(scaled_img, rotation)
    rotated_rect = rotated_bg.get_rect(center=(position[0] + width // 2, position[1] + height // 2))

    board_surface.blit(rotated_bg, rotated_rect.topleft)


# --------------------
# Example usage
# --------------------
def main():
    running = True
    while running:
        screen.fill(BG)

        # FRONT-FACING CARDS
        draw_card(screen, [1, None, 0], position=(100, 20), size=(180, 260), rotation=0)
        draw_card(screen, [None, 1, 1], position=(350, 50), size=(180, 260), rotation=15)
        draw_card(screen, [0, 1, None], position=(600, 80), size=(180, 260), rotation=-10)

        # BACK-FACING CARDS
        draw_card_back(screen, bg_image, position=(200, 350), size=(180, 260), rotation=5)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
