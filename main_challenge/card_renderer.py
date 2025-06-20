import pygame
import sys
import os

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

# ----------------------
# Draw front of card
# ----------------------


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

def draw_card_front(board_surface, bits, position, size, rotation=0, card_type="state", measurement_img=measurement_img):
    """
    Draws a card (state, operator, or measurement) with optional rotation.
    - board_surface: main surface to draw onto
    - bits: list of 3 values (int, str, or None)
    - position: (x, y) top-left position on the board
    - size: (width, height) of the card
    - rotation: angle in degrees (clockwise)
    - card_type: "state", "operator", or "measurement"
    - measurement_img: optional Surface to render when value == "M"
    """
    width, height = size
    card_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(card_surface, CARD_COLOR, card_surface.get_rect().inflate(-20, -20), border_radius=20)

    n = len(bits)
    radius = int(min(width, height) * 0.15)

    # Margins and spacing
    top_margin = int(height * 0.18)
    bottom_margin = int(height * 0.18)
    total_height = height - top_margin - bottom_margin
    spacing = total_height / (n - 1 if n > 1 else 1)

    # Color gradients based on card type
    if card_type == "operator":
        color_top = pygame.Color(100, 149, 237)     # cornflower blue
        color_bottom = pygame.Color(180, 220, 255)  # light blue
    elif card_type == "measurement":
        color_top = pygame.Color(138, 43, 226)      # blue violet
        color_bottom = pygame.Color(200, 160, 255)  # light purple
    else:  # "state"
        color_top = pygame.Color(250, 128, 114)     # salmon pink
        color_bottom = pygame.Color(255, 224, 230)

    for i, value in enumerate(bits):
        y = top_margin + i * spacing
        x = width // 2
        t = i / (n - 1) if n > 1 else 0

        # Draw horizontal line if not None and operator/measurement
        if card_type in ("operator", "measurement") and value is not None:
            line_margin = int(width * 0.15)
            line_y = int(y)
            pygame.draw.line(
                card_surface,
                (200, 200, 200),  # light gray
                (line_margin, line_y),
                (width - line_margin, line_y),
                width=2
            )

        if value is None:
            draw_blur_circle(card_surface, (x, int(y)), radius)
        else:
            color = lerp_color(color_top, color_bottom, t)

            if card_type in ("operator", "measurement"):
                # Draw square
                rect = pygame.Rect(0, 0, radius * 2, radius * 2)
                rect.center = (x, int(y))
                pygame.draw.rect(card_surface, color, rect)
            else:
                # Draw circle
                pygame.draw.circle(card_surface, color, (x, int(y)), radius)

            # Draw text or measurement image
            if str(value) == "M" and measurement_img:
                img_size = int(radius * 1.4)
                img = pygame.transform.smoothscale(measurement_img, (img_size, img_size))
                img_rect = img.get_rect(center=(x, int(y)))
                card_surface.blit(img, img_rect)
            else:
                font_size = int(radius * 1.5)
                font = pygame.font.SysFont("arial", font_size, bold=False)
                text = font.render(str(value), True, TEXT_COLOR)
                text_rect = text.get_rect(center=(x, int(y)))
                card_surface.blit(text, text_rect)

    # Rotate and blit onto the main board
    rotated_surface = pygame.transform.rotate(card_surface, rotation)
    rotated_rect = rotated_surface.get_rect(center=(position[0] + width // 2, position[1] + height // 2))
    board_surface.blit(rotated_surface, rotated_rect.topleft)






# -------------------- 
# Draw back of card
# -------------------- 
def apply_rounded_mask(surface, border_radius):
    """
    Applies a rounded corner mask to the given surface using BLEND_RGBA_MULT.
    """
    mask = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=border_radius)
    surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

def draw_card_back(board_surface, bg_image, position, size, rotation=0):
    """
    Draws a card back with rounded corners.
    - board_surface: surface to draw onto
    - bg_image: the preloaded card background image (Surface)
    - position: (x, y) top-left corner on the board
    - size: (width, height) of the card
    - rotation: rotation angle in degrees
    """
    width, height = size

    scaled_img = pygame.transform.smoothscale(bg_image.copy(), (width, height))

    apply_rounded_mask(scaled_img, border_radius=20)

    rotated_img = pygame.transform.rotate(scaled_img, rotation)
    rotated_rect = rotated_img.get_rect(center=(position[0] + width // 2, position[1] + height // 2))

    board_surface.blit(rotated_img, rotated_rect.topleft)



# --------------------
# Example usage
# --------------------
def main():
    running = True
    while running:
        screen.fill(BG)

        # FRONT-FACING CARDS
        draw_card_front(screen, ["C", "I", "X"], position=(100, 20), size=(180, 260), rotation=0, card_type="operator")
        draw_card_front(screen, ["M", None, None], position=(350, 50), size=(180, 260), rotation=0, card_type="measurement")
        draw_card_front(screen, [1, None, None], position=(600, 80), size=(180, 260), rotation=0)

        # BACK-FACING CARDS
        draw_card_back(screen, bg_image, position=(120, 300), size=(180, 260), rotation=5)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
