import pygame
import sys
from constants import *

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Select Time Per Move")

FONT = pygame.font.SysFont(None, 32)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)

# Input box
input_box = pygame.Rect(200, 140, 200, 40)
active = False
user_text = ""

# Buttons
add_button = pygame.Rect(180, 220, 100, 50)
no_time_button = pygame.Rect(320, 220, 120, 50)

selected_time = None   # This will store the result


def draw_text(text, font, color, surface, x, y):
    img = font.render(text, True, color)
    surface.blit(img, (x, y))


def time_dialog():
    global active, user_text, selected_time

    while True:
        screen.fill(MAIN_BACKGROUND_COLOR)
        #outside box
        pygame.draw.rect(screen,(13, 18, 36),[130,60,360,250])
        pygame.draw.rect(screen,CAPTURED_BG,[130,60,360,250],2)

        # Title
        draw_text("Enter Time per move", FONT,TEXT_COLOR_FOR_HEADINGS, screen, 180, 80)

        # Input box
        pygame.draw.rect(screen, CONTENT_CONTAINER_BG if active else CONTAINER_BOX_BG, input_box)
        text_surface = FONT.render(user_text, True, BLACK)
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 8))

        # Buttons
        pygame.draw.rect(screen, BUTTON_BACK_GROUND_COLOR, [180, 220, 100, 50],border_radius=20)
        pygame.draw.rect(screen, BUTTON_BACK_GROUND_BORDER,[180, 220, 100, 50],2,border_radius=20)
        pygame.draw.rect(screen,  BUTTON_BACK_GROUND_COLOR, [320, 220, 120, 50],border_radius=20)
        pygame.draw.rect(screen,BUTTON_BACK_GROUND_BORDER, [320, 220, 120, 50],2,border_radius=20)

        draw_text("Add", FONT, BLACK, screen, add_button.x + 25, add_button.y + 15)
        draw_text("No Time", FONT, BLACK, screen, no_time_button.x + 15, no_time_button.y + 15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False

                if add_button.collidepoint(event.pos):
                    if user_text.isdigit():
                        selected_time = int(user_text)
                        return selected_time

                if no_time_button.collidepoint(event.pos):
                    selected_time = None  # Infinite time
                    return selected_time

            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.unicode.isdigit():
                    user_text += event.unicode

        pygame.display.flip()


# Run dialog
time_limit = time_dialog()

print("Selected Time:", time_limit)
