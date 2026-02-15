import pygame
pygame.init()

import os, sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class SoundManager:
    def __init__(self):
        self.sounds = {
            "move": pygame.mixer.Sound(resource_path("assets/sound/move-self.mp3")),
            "capture": pygame.mixer.Sound(resource_path("assets/sound/capture.mp3")),
            "error": pygame.mixer.Sound(resource_path("assets/sound/phone-vibration-96623 (1).mp3")),
            
            "checkmate": pygame.mixer.Sound(resource_path("assets/sound/checkmate.mp3")),
            "Lost": pygame.mixer.Sound(resource_path("assets/sound/gameLost.mp3")),
            "click": pygame.mixer.Sound(resource_path("assets/sound/button.mp3")),
        }

        for s in self.sounds.values():
            s.set_volume(0.6)

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()
sound= SoundManager()

WIDTH = 1300
HEIGHT = 640
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption('CheckMate')
font = pygame.font.Font('freesansbold.ttf', 20)
small_font = pygame.font.Font('freesansbold.ttf', 16)

medium_font = pygame.font.Font('freesansbold.ttf', 23)
Semimedium_font = pygame.font.Font('freesansbold.ttf', 25)
big_font = pygame.font.Font('freesansbold.ttf', 30)
timer = pygame.time.Clock()
fps = 60



matrix_size = 90 
cell_size = 30 
padding = 2       

# Define positions for 4 matrices

matrix_positions = [(1098, 484), (1166, 484), (1098, 552), (1166, 552)]
WHITE=(255,255,255)

GREEN =  [(210, 210, 210), (69, 139, 0)]
BLUE  =  [(170, 200, 230) ,(70, 90, 130)]
PINK  =   [(245, 210, 220), (170, 105, 130)]
BROWN =  [(240, 217, 181), (181, 136, 99)]

matrix_colors = [
    [GREEN[1],GREEN[0],GREEN[0], GREEN[1]],
    [BLUE[1],BLUE[0], BLUE[0], BLUE[1]],
    [PINK[1], PINK[0],PINK[0], PINK[1]],
    [BROWN[1], BROWN[0],BROWN[0], BROWN[1]]
    
]
board_color_location=[(0,0),(1,0),(0,1),(1,1)]
board_color_location_sf=[(10,3),(11,3),(10,5),(11,5)]


# game variables and images
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
captured_pieces_white = []
captured_pieces_black = []
# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
selection = 100
valid_moves = []
# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
black_queen = pygame.image.load(resource_path("assets/images/black queen.png" ))
black_queen = pygame.transform.scale(black_queen, (50, 50))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))
black_king = pygame.image.load(resource_path("assets/images/black king.png" ))
black_king = pygame.transform.scale(black_king, (50, 50))
black_king_small = pygame.transform.scale(black_king, (45, 45))
black_rook = pygame.image.load(resource_path("assets/images/black rook.png" ))
black_rook = pygame.transform.scale(black_rook, (50, 50))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))
black_bishop = pygame.image.load(resource_path("assets/images/black bishop1.png" ))
black_bishop = pygame.transform.scale(black_bishop, (50, 50))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
black_knight = pygame.image.load(resource_path("assets/images/black knight.png" ))
black_knight = pygame.transform.scale(black_knight, (50, 50))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))
black_pawn = pygame.image.load(resource_path("assets/images/black pawn.png" ))
black_pawn = pygame.transform.scale(black_pawn, (45, 45))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))
white_queen = pygame.image.load(resource_path("assets/images/white queen.png" ))
white_queen = pygame.transform.scale(white_queen, (50, 50))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))
white_king = pygame.image.load(resource_path("assets/images/white king.png" ))
white_king = pygame.transform.scale(white_king, (50, 50))
white_king_small = pygame.transform.scale(white_king, (45, 45))
white_rook = pygame.image.load(resource_path("assets/images/white rook.png" ))
white_rook = pygame.transform.scale(white_rook, (50, 50))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))
white_bishop = pygame.image.load(resource_path("assets/images/white bishop1.png" ))
white_bishop = pygame.transform.scale(white_bishop, (50, 50))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
white_knight = pygame.image.load(resource_path("assets/images/white knight.png" ))
white_knight = pygame.transform.scale(white_knight, (50, 50))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))
white_pawn = pygame.image.load(resource_path("assets/images/white pawn.png" ))
white_pawn = pygame.transform.scale(white_pawn, (45, 45))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
white_promotions = ['bishop', 'knight', 'rook', 'queen']
white_moved = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]
black_promotions = ['bishop', 'knight', 'rook', 'queen']
black_moved = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
# check variables/ flashing counter
counter = 0
winner = ''
game_over = False
white_ep = (100, 100)
black_ep = (100, 100)
white_promote = False
black_promote = False
promo_index = 100
check = False
castling_moves = []
evolve_promo_name=""


want_to_save=False
SAVE_DIR = r"D:\\CheckMate\\Stored_math"
# BOARD COLOR VAR COLOR [(light, dark)]
possible_board_color = [

[(210, 210, 210), (69, 139, 0)],
[(170, 200, 230) ,(70, 90, 130)],
[(245, 210, 220), (170, 105, 130)],
[(240, 217, 181), (181, 136, 99)]
]


#BG VARIATIONS
CAPTURED_BG_variations = [
    (20, 40, 32),   # GREEN
    (40, 45, 70),   # BLUE
    (60, 35, 45),   # PINK
    (48, 36, 28)    # BROWN
]

CONTAINER_BOX_BG_variations = [
    (26, 64, 50),   # GREEN
    (27, 30, 82),   # BLUE
    (80, 30, 55),   # PINK
    (64, 48, 36)    # BROWN
]

CONTAINER_BOX_BORDER_variations = [
    (110, 190, 150), # GREEN
    (13, 18, 36),    # BLUE
    (120, 60, 90),   # PINK
    (200, 170, 120)   # BROWN
]

#inner
CONTENT_CONTAINER_BG_variation = [
    (34, 82, 64),   # GREEN
    (35, 50, 80),   # BLUE
    (100, 45, 70),  # PINK
    (82, 64, 48)    # BROWN
]

CONTENT_CONTAINER_BG_BORDER_variation = [
    (170, 235, 205), # GREEN
    (90, 120, 160),  # BLUE
    (180, 120, 150), # PINK
    (200, 170, 120)    # BROWN
]



#analysis or quality pannel and bg
MAIN_BACKGROUND_COLOR_variation = [
    (6, 16, 12),   # GREEN
    (4, 4, 8),     # BLUE
    (10, 4, 8),    # PINK
    (28, 20, 14)   # BROWN
]

MAIN_QUALITY_PANNEL_BG_variation = [
    (20, 40, 32),  # GREEN
    (20, 26, 52),  # BLUE
    (70, 25, 45),  # PINK
    (48, 36, 28)   # BROWN
]


# button back ground color
BUTTON_BACK_GROUND_COLOR_variation = [
    (72, 155, 122),  # GREEN
    (45, 85, 145),   # BLUE
    (160, 80, 120),  # PINK
    (120, 90, 60)    # BROWN
]

BUTTON_BACK_GROUND_BORDER_variation = [
    (185, 245, 215), # GREEN
    (120, 180, 240), # BLUE
    (240, 170, 200), # PINK
    (230, 205, 165)  # BROWN
]

#text
TEXT_COLOR_FOR_HEADINGS_variation = [
    (185, 245, 215), # GREEN
    (120, 180, 240), # BLUE
    (240, 170, 200), # PINK
    (230, 205, 165) # BROWN
]


DULL_TEXT_COLOR_variation = [
    (100, 130, 115),  # GREEN
    (110, 120, 145),  # BLUE
    (140, 110, 125),  # PINK
    (120, 110, 95)    # BROWN
]
BUTTON_HOVER_COLOR_variatio = [
    (115, 195, 165),  # GREEN hover (lighter)
    (90, 130, 190),   # BLUE hover
    (200, 130, 165),  # PINK hover
    (165, 135, 105)   # BROWN hover
]



# squares (classic brown board)
desired_color_dark = (181, 136, 99)
desired_color_light = (240, 217, 181)

# backgrounds
CAPTURED_BG = (48, 36, 28)

CONTAINER_BOX_BG = (64, 48, 36)
CONTAINER_BOX_BORDER = (160, 130, 90)

CONTENT_CONTAINER_BG = (82, 64, 48)
CONTENT_CONTAINER_BG_BORDER = (200, 170, 120)



TEXT_COLOR_FOR_HEADINGS = (230, 205, 165)


#wanted color changing varibles
#squares
desired_color_dark= (70, 90, 130) 
desired_color_light= (170, 200, 230)
#backgrounds
CAPTURED_BG = (40, 45, 70)

CONTAINER_BOX_BG= (27, 30, 82)
CONTAINER_BOX_BORDER  = (13, 18, 36)

CONTENT_CONTAINER_BG=(35, 50, 80)
CONTENT_CONTAINER_BG_BORDER=(90, 120, 160)

MAIN_BACKGROUND_COLOR=(4, 4, 8)

MAIN_QUALITY_PANNEL_BG=(20, 26, 52)

TEXT_COLOR_FOR_HEADINGS=(120, 180, 240)
BUTTON_BACK_GROUND_COLOR=(45,85,145)
BUTTON_BACK_GROUND_BORDER=(120, 180, 240)
DULL_TEXT=(140, 160, 190)


BUTTON_HOVER_COLOR= (70, 110, 170)
sound_once=True
# function to check all pieces valid options on board
def check_options(pieces, locations, turn):
    global castling_moves
    moves_list = []
    all_moves_list = []
    castling_moves = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list, castling_moves = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list


# check king valid moves
def check_king(position, color):
    moves_list = []
    castle_moves = check_castling()
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for kings, they can go one square any direction
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list, castle_moves


# check queen valid moves
def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list


# check bishop moves
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# check rook moves
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# check valid pawn moves
def check_pawn(position, color):
    
    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
            # indent the check for two spaces ahead, so it is only checked if one space ahead is also open
            if (position[0], position[1] + 2) not in white_locations and \
                    (position[0], position[1] + 2) not in black_locations and position[1] == 1:
                moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
        # add en passant move checker
        if (position[0] + 1, position[1] + 1) == black_ep:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) == black_ep:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
            # indent the check for two spaces ahead, so it is only checked if one space ahead is also open
            if (position[0], position[1] - 2) not in white_locations and \
                    (position[0], position[1] - 2) not in black_locations and position[1] == 6:
                moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
        # add en passant move checker
        if (position[0] + 1, position[1] - 1) == white_ep:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) == white_ep:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list


# check valid knight moves
def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


# check for valid moves for just selected piece
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options


# draw valid moves on screen
def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 75 + 50), 5)


# draw captured pieces on side of screen
def draw_captured():
    j=0
    k=0
    for i in range(len(captured_pieces_white)):
        if captured_pieces_white[i]=="pawn":
            captured_piece = captured_pieces_white[i]
            index = piece_list.index(captured_piece)
            screen.blit(small_black_images[index], (825, 100 + 50 * j))
            j += 1
        else:
            captured_piece = captured_pieces_white[i]
            index = piece_list.index(captured_piece)
            screen.blit(small_black_images[index], (875,100+ 50 * k))
            k+=1
    j=0
    k=0
    for i in range(len(captured_pieces_black)):
        if captured_pieces_black[i]=="pawn":
            captured_piece = captured_pieces_black[i]
            index = piece_list.index(captured_piece)
            screen.blit(small_white_images[index], (925, 100 + 50 * j))
            j +=1
        else:
            captured_piece = captured_pieces_black[i]
            index = piece_list.index(captured_piece)
            screen.blit(small_white_images[index], (975, 100+ 50 * k))
            k +=1


# draw a flashing square around king if in check
def draw_check():
    global check
    check = False
    
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    check = True
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * 100 + 1,
                                                              white_locations[king_index][1] * 75 + 1, 100, 75], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    check = True
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * 100 + 1,
                                                               black_locations[king_index][1] * 75 + 1, 100, 75], 5)


def draw_game_over():
    winner="black"
    pygame.draw.rect(screen, CONTAINER_BOX_BG, [200, 200, 400, 200],border_radius=20)
    pygame.draw.rect(screen,CONTENT_CONTAINER_BG_BORDER, [200, 200, 400, 200],10,border_radius=20)
    screen.blit(big_font.render(f'{winner} won the GAME!', True, TEXT_COLOR_FOR_HEADINGS), (250,250))
    screen.blit(font.render(f'Press ENTER to EXIT', True, DULL_TEXT), (290, 300))


# check en passant because people on the internet won't stop bugging me for it
def check_ep(old_coords, new_coords):
    if turn_step <= 1:
        index = white_locations.index(old_coords)
        ep_coords = (new_coords[0], new_coords[1] - 1)
        piece = white_pieces[index]
    else:
        index = black_locations.index(old_coords)
        ep_coords = (new_coords[0], new_coords[1] + 1)
        piece = black_pieces[index]
    if piece == 'pawn' and abs(old_coords[1] - new_coords[1]) > 1:
        # if piece was pawn and moved two spaces, return EP coords as defined above
        pass
    else:
        ep_coords = (100, 100)
    return ep_coords


# add castling
def check_castling():
    # king must not currently be in check, neither the rook nor king has moved previously, nothing between
    # and the king does not pass through or finish on an attacked piece
    castle_moves = []  # store each valid castle move as [((king_coords), (castle_coords))]
    rook_indexes = []
    rook_locations = []
    king_index = 0
    king_pos = (0, 0)
    if turn_step > 1:
        for i in range(len(white_pieces)):
            if white_pieces[i] == 'rook':
                rook_indexes.append(white_moved[i])
                rook_locations.append(white_locations[i])
            if white_pieces[i] == 'king':
                king_index = i
                king_pos = white_locations[i]
        if not white_moved[king_index] and False in rook_indexes and not check:
            for i in range(len(rook_indexes)):
                castle = True
                if rook_locations[i][0] > king_pos[0]:
                    empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
                                     (king_pos[0] + 3, king_pos[1])]
                else:
                    empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
                for j in range(len(empty_squares)):
                    if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
                            empty_squares[j] in black_options or rook_indexes[i]:
                        castle = False
                if castle:
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    else:
        for i in range(len(black_pieces)):
            if black_pieces[i] == 'rook':
                rook_indexes.append(black_moved[i])
                rook_locations.append(black_locations[i])
            if black_pieces[i] == 'king':
                king_index = i
                king_pos = black_locations[i]
        if not black_moved[king_index] and False in rook_indexes and not check:
            for i in range(len(rook_indexes)):
                castle = True
                if rook_locations[i][0] > king_pos[0]:
                    empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
                                     (king_pos[0] + 3, king_pos[1])]
                else:
                    empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
                for j in range(len(empty_squares)):
                    if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
                            empty_squares[j] in white_options or rook_indexes[i]:
                        castle = False
                if castle:
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    return castle_moves


def draw_castling(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0][0] * 100 + 50, moves[i][0][1] * 100 + 70), 8)
        screen.blit(font.render('king', True, 'black'), (moves[i][0][0] * 100 + 30, moves[i][0][1] * 100 + 70))
        pygame.draw.circle(screen, color, (moves[i][1][0] * 100 + 50, moves[i][1][1] * 100 + 70), 8)
        screen.blit(font.render('rook', True, 'black'),
                    (moves[i][1][0] * 100 + 30, moves[i][1][1] * 100 + 70))
        pygame.draw.line(screen, color, (moves[i][0][0] * 100 + 50, moves[i][0][1] * 75 + 70),
                         (moves[i][1][0] * 100 + 50, moves[i][1][1] * 75 + 70), 2)

