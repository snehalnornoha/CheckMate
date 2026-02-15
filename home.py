import pygame
import subprocess
import sys
from constants import resource_path


# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1300, 640
font = pygame.font.SysFont(None, 48)
button_font = pygame.font.SysFont(None, 36)
pannel = pygame.image.load(resource_path("assets/images/HOMEPAGE1.png"))
pannel = pygame.transform.scale(pannel, (1300, 660))
def blur_rect(surface, rect, scale=0.02):
    sub = surface.subsurface(rect).copy()
    small = pygame.transform.smoothscale(
        sub, (max(1, int(rect.width * scale)), max(1, int(rect.height * scale)))
    )
    blurred = pygame.transform.smoothscale(small, rect.size)
    surface.blit(blurred, rect.topleft)

def draw_button(rect, text, mouse_pos, mouse_pressed, surface):
    base_color = (20, 26, 52)
   
    text_color = (120, 180, 240)

    color = base_color

    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(surface, color, rect, border_radius=30)
        draw_text(text, button_font, text_color, surface, rect.centerx, rect.centery)
        
    else:
        blur_rect(surface, rect,0.05)
        pygame.draw.rect(surface, color, rect, 3, border_radius=16)
        draw_text(text, button_font,(0,0,0), surface, rect.centerx, rect.centery)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def start_game(script_name):
    pygame.display.quit()  # Close the menu window

    if getattr(sys, 'frozen', False):
        # Running as EXE → run other EXE
        exe_name = script_name.replace(".py", ".exe")
        subprocess.run([exe_name])
    else:
        # Running as Python → run .py
        subprocess.run([sys.executable, script_name])

    pygame.display.init()
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CheckMate - Home")

def main_menu():
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CheckMate - Home")
    btn_single = pygame.Rect(WIDTH // 2 - 150, 250, 300, 60)
    btn_multi = pygame.Rect(WIDTH // 2 - 150, 340, 300, 60)
    btn_analyzer = pygame.Rect(WIDTH // 2 - 150, 430, 300, 60)
    btn_exit = pygame.Rect(WIDTH // 2 - 150, 520, 300, 60)


    run=True
    while  run:
        
        screen.blit(pannel, (0, 0))
        
        mx, my = pygame.mouse.get_pos()

        
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        draw_button(btn_single, "Stockfish Arena", mouse_pos, mouse_pressed, screen)
        draw_button(btn_multi, "Smart Match", mouse_pos, mouse_pressed, screen)
        draw_button(btn_analyzer, "Analysis Lab", mouse_pos, mouse_pressed, screen)
        draw_button(btn_exit, "Exit", mouse_pos, mouse_pressed, screen)
         


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    
                    if btn_single.collidepoint((mx, my)):
                        start_game(resource_path("main1.py"))
                    elif btn_multi.collidepoint((mx, my)):
                        start_game(resource_path("multi_player.py"))
                    elif btn_analyzer.collidepoint((mx, my)):
                        start_game(resource_path("self_analyzer.py"))
                    elif btn_exit.collidepoint((mx, my)):
                        run=False

        pygame.display.update()

if __name__ == "__main__":
    main_menu()