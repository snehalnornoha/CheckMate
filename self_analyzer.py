# two player chess in python with Pygame!
# pawn double space checking
# castling
# en passant
# pawn promotion

import pygame
from constants import *
from constants import sound
import os
import re

# Ensure directory exists
os.makedirs(SAVE_DIR, exist_ok=True)
print("-------------",SAVE_DIR)


pygame.display.set_caption("Save File")

FONT = pygame.font.SysFont(None, 30)
BIG_FONT = pygame.font.SysFont(None, 36)



# center horizontally, middle vertically
input_box = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 60, 300, 45)

save_button = pygame.Rect(WIDTH//2 - 170, HEIGHT//2 + 10, 140, 45)
cancel_button = pygame.Rect(WIDTH//2 + 30, HEIGHT//2 + 10, 140, 45)


filename = ""
active = False
message = ""
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
GREEN = (0, 180, 0)
RED = (180, 0, 0)

pygame.init()

square_map=[['h1', 'g1', 'f1', 'e1', 'd1', 'c1', 'b1', 'a1'] ,
['h2', 'g2', 'f2', 'e2', 'd2', 'c2', 'b2', 'a2'] ,
['h3', 'g3', 'f3', 'e3', 'd3', 'c3', 'b3', 'a3'] ,
['h4', 'g4', 'f4', 'e4', 'd4', 'c4', 'b4', 'a4'] ,
['h5', 'g5', 'f5', 'e5', 'd5', 'c5', 'b5', 'a5'] ,
['h6', 'g6', 'f6', 'e6', 'd6', 'c6', 'b6', 'a6'] ,
['h7', 'g7', 'f7', 'e7', 'd7', 'c7', 'b7', 'a7'] ,
['h8', 'g8', 'f8', 'e8', 'd8', 'c8', 'b8', 'a8'] ]



history_of_white_locs= list()
history_of_white_pieces =list()
history_of_white_moved=list()
history_of_black_locs=list()
history_of_black_pieces= list()
history_of_black_moved=list()
history_captured_pieces_white=list()
history_captured_pieces_black=list()
history_everymove=list()
his_white_material_score=list()
his_black_material_score=list()
white_material_score=0
black_material_score=0

history_of_white_locs.append(white_locations.copy())
history_of_white_pieces.append(white_pieces.copy())
history_of_white_moved.append(white_moved.copy())
history_captured_pieces_white.append(captured_pieces_white.copy())

history_captured_pieces_black.append(captured_pieces_black.copy())
history_of_black_locs.append(black_locations.copy())
history_of_black_pieces.append(black_pieces.copy())
history_of_black_moved.append(white_moved.copy())
his_black_material_score.append(black_material_score)
his_white_material_score.append(white_material_score)


history_of_board_white=list()
history_of_board_black=list()
history_of_move={}


def undo_the_move():
    global white_locations, black_locations, white_pieces, black_pieces,history_of_set_move
    global white_moved, black_moved, turn_step, selection, valid_moves,set_of_numbers,white_material_score,black_material_score
    global white_options, black_options,history_everymove,evrymove_name_list,set_of_move
    global history_of_white_locs,history_of_white_pieces,history_of_white_moved,his_black_material_score
    global history_of_black_locs,history_of_black_pieces,history_of_black_moved,his_white_material_score
    global history_captured_pieces_white,history_captured_pieces_black,captured_pieces_black,captured_pieces_white
    
    # We need at least 2 states (initial + 1 move) to undo back to start
    if len(history_everymove)==1 and turn_step==0:
        set_of_numbers=set_of_numbers-1
        history_everymove.pop()
        evrymove_name_list=[]
    if len(history_everymove)>1 and turn_step==0:
        history_everymove.pop()
        set_of_numbers=set_of_numbers-1

        evrymove_name_list=history_everymove[-1].copy()
    



    if len(history_of_white_locs) > 1:
        sound.play("move")
    
        # Remove the current state
        history_of_white_locs.pop()
        history_of_white_pieces.pop()
        history_of_white_moved.pop()
        history_of_black_locs.pop()
        history_of_black_pieces.pop()
        history_of_black_moved.pop()
        history_captured_pieces_white.pop()
        history_captured_pieces_black.pop()
        history_of_set_move.pop()
        
        
        

        # Restore to the now-last state in history
        white_locations = history_of_white_locs[-1].copy()
        white_pieces = history_of_white_pieces[-1].copy()
        white_moved = history_of_white_moved[-1].copy()
        captured_pieces_white=history_captured_pieces_white[-1].copy()
        captured_pieces_black=history_captured_pieces_black[-1].copy()
        black_locations = history_of_black_locs[-1].copy()
        black_pieces = history_of_black_pieces[-1].copy()
        black_moved = history_of_black_moved[-1].copy()
        set_of_move = history_of_set_move[-1]
        
       
        
        
        if turn_step <=1:
            turn_step=2
            if len(his_black_material_score) >= 2:
                his_black_material_score.pop()
                black_material_score=his_black_material_score[-1]
        else: 
            turn_step=0
            if len(his_white_material_score)>=2:
                his_white_material_score.pop()
                white_material_score=his_white_material_score[-1]
        
        
        # Reset selection state
        selection = 100
        valid_moves = []
        
        # RE-CALCULATE options so the game knows where pieces are now
        black_options = check_options(black_pieces, black_locations, 'black')
        white_options = check_options(white_pieces, white_locations, 'white')
evrymove_name_list=list()
generated_move="moves"
set_of_move=""
set_of_numbers=1
history_of_set_move=list()
history_of_set_move.append(set_of_move)
#calcu;ate the material score
def material_score(name_of_piece):
    print(name_of_piece)
    if name_of_piece == 'pawn':
        return 1
    elif name_of_piece == 'rook':
        return 5
    elif name_of_piece =='queen':
        return 9
    elif name_of_piece in ['knight','bishop']:
        return 3


def save_to_file(name, text):
    try:
        print(name,text)
        if not name.endswith(".txt"):
            name += ".txt"

        full_path = os.path.join(SAVE_DIR, name)

        with open(full_path, "w") as f:
            f.write(text)

    except Exception as e:
        print("Save error:", e)


#naming the move
def name_of_move(half_move,temp_x,temp_y,isBlack):
    global set_of_move,set_of_numbers,history_everymove,history_of_set_move
    temp_move= square_map[temp_y][temp_x]
    
    if isBlack:
        temp_index = white_locations.index((temp_x,temp_y))
        temp_piece=white_pieces[temp_index]
    else:
        temp_index = black_locations.index((temp_x,temp_y))
        temp_piece=black_pieces[temp_index]
    if temp_piece!='pawn' and temp_piece != 'knight':
        temp_move=temp_piece[0].upper()+temp_move
    elif temp_piece == 'knight':
        temp_move='N'+temp_move
    temp_move=str(half_move+temp_move)
    
    if half_move is not "" and isBlack:
        set_of_move=" "+str(set_of_numbers)+". "+temp_move
        history_of_set_move.append(set_of_move)
        set_of_numbers = set_of_numbers+1
    elif half_move is not "" and not isBlack:
        set_of_move=set_of_move+", "+temp_move
        history_of_set_move.append(set_of_move)
        evrymove_name_list.append(set_of_move)
        history_everymove.append(evrymove_name_list.copy())
        

    return temp_move


# static surace 
board_surface=pygame.Surface((WIDTH-30,HEIGHT))

def draw_static_board(surface):
   
    undo_pannel=pygame.image.load(resource_path("assets/images/undo.png"))
    undo_pannel=pygame.transform.scale(undo_pannel,(40,40))
    surface.fill(MAIN_QUALITY_PANNEL_BG)
    pygame.draw.rect(surface, desired_color_light, [0,0, 800,HEIGHT])
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(surface,desired_color_dark, [600 - (column * 200), row *75,100,75])
        else:
            pygame.draw.rect(surface,desired_color_dark, [700 - (column * 200), row *75,100,75])
    

   
    

    

    for i in range(9):
        pygame.draw.line(surface,"black", (0, 75 * i), (800, 75 * i), 2)
        pygame.draw.line(surface, "black", (100 * i, 0), (100 * i, 600), 2)

    
  

    pygame.draw.rect(surface, CAPTURED_BG, [806,0, 240,HEIGHT])
    
    pygame.draw.line(surface, MAIN_BACKGROUND_COLOR, (835,50),(1017,50), 1)
    pygame.draw.rect(surface,MAIN_BACKGROUND_COLOR , [0, 602, 802, 40], 5)
    pygame.draw.rect(surface,MAIN_BACKGROUND_COLOR , [802, 0, 468, HEIGHT],5)
    
    pygame.draw.line(surface,  MAIN_BACKGROUND_COLOR , (1048, 0),(1048,HEIGHT), 5)
    #undo button
    pygame.draw.rect(surface,BUTTON_BACK_GROUND_COLOR, [1076,340, 160, 75],border_radius=20)
    pygame.draw.rect(surface,BUTTON_BACK_GROUND_BORDER, [1076,340, 160, 75],3,border_radius=20)
    surface.blit(undo_pannel,(1090, 356))
    #save button(92, 58, 34)
    pygame.draw.rect(surface,BUTTON_BACK_GROUND_COLOR , [1076,260, 160, 75],border_radius=20)
    pygame.draw.rect(surface,BUTTON_BACK_GROUND_BORDER, [1076,260, 160, 75],3,border_radius=20)
    #history of move (60, 60, 60) (85, 85, 85)
    pygame.draw.rect(surface, CONTAINER_BOX_BG, [1060, 20, 200, 46],border_radius=20)
    pygame.draw.rect(surface,CONTAINER_BOX_BORDER, [1060, 20, 200, 46], 2,border_radius=20)
    pygame.draw.rect(surface,  CONTENT_CONTAINER_BG, [1070, 70, 180, 140],border_radius=2)
    pygame.draw.rect(surface,  CONTENT_CONTAINER_BG_BORDER , [1070, 70, 180, 140], 3,border_radius=2)

    #the button templete for color change 
    pygame.draw.rect(surface,CONTAINER_BOX_BG, [1060, 434, 200, 196],border_radius=2)
    pygame.draw.rect(surface,CONTAINER_BOX_BORDER, [1060, 434, 200, 196], 3,border_radius=2)
    pygame.draw.rect(surface, CONTENT_CONTAINER_BG , [1092,478, 140, 140],border_radius=2)
    pygame.draw.rect(surface, CONTENT_CONTAINER_BG_BORDER , [1090,476, 146, 146],4,border_radius=2)
    
    

    
    for pos, colors in zip(matrix_positions, matrix_colors):
        for i in range(2):
            for j in range(2):
                color = colors[i * 2 + j]
                rect = pygame.Rect(pos[0] + j * (cell_size + padding), pos[1] + i * (cell_size + padding), cell_size, cell_size)
                pygame.draw.rect(surface,color, rect)
        
# draw main game board
def draw_board():
    if not want_to_save:
   
    
        screen.blit(board_surface,(0,0))
        

        
        
        screen.blit(Semimedium_font.render('UNDO', True, TEXT_COLOR_FOR_HEADINGS), (1125, 366))
        screen.blit(Semimedium_font.render('SAVE', True,  TEXT_COLOR_FOR_HEADINGS), (1125, 286))
        screen.blit(Semimedium_font.render('COLORS', True, TEXT_COLOR_FOR_HEADINGS), (1105, 446))
        screen.blit(Semimedium_font.render("CAPTURED", True, TEXT_COLOR_FOR_HEADINGS), (854,22))
        screen.blit(Semimedium_font.render("PastMoves", True,  TEXT_COLOR_FOR_HEADINGS), (1096,32))
        
        status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                        'Black: Select a Piece to Move!', 'Black: Select a Destination!',"Select Piece to Promote Pawn"]
                        
        screen.blit(font.render(status_text[turn_step], True, 'black'), (10, 610))
    
        screen.blit(medium_font.render('FORFEIT', True, 'black'), (810, 830))
        if white_promote or black_promote:
            pygame.draw.rect(screen, 'gray', [0, 600,600,40])
            screen.blit(font.render(status_text[4], True, 'black'), (10, 610))
        #material score board
        screen.blit(font.render(f"white: {white_material_score}", True, desired_color_light), (823,75))
        screen.blit(font.render(f"black: {black_material_score}", True,desired_color_dark), (946,75))

        length_of_move=len(evrymove_name_list)
        
        if length_of_move is not 0:
            if length_of_move <=6:
                for i  in range(0,length_of_move):
                    screen.blit(small_font.render(evrymove_name_list[i], True, DULL_TEXT),(1080, 80+(i*20)))
            elif length_of_move >6:
                for i  in range(0,6):
                    temp_length=length_of_move-6 
                    screen.blit(small_font.render(evrymove_name_list[temp_length+i], True, DULL_TEXT),(1080, 82+(i*20)))
        else:
            screen.blit(small_font.render("no move yet", True, DULL_TEXT),(1110, 110))
        
         
        if len(captured_pieces_white) ==  0 and len(captured_pieces_black) ==  0:
            screen.blit(small_font.render("No pieces captured", True, DULL_TEXT),(850, 320))
            
    elif want_to_save:
        screen.fill(MAIN_QUALITY_PANNEL_BG)
        
        title = BIG_FONT.render("Enter file name:", True, BLACK)
        
        pygame.draw.rect(screen, (100,100,100), [420, 140, 460, 300])
        pygame.draw.rect(screen, "black", [420, 140, 460, 300], 2)
        screen.blit(title, (540,200))

        box_color = GREEN if active else GRAY
        pygame.draw.rect(screen, box_color, input_box, 2)

        txt_surface = FONT.render(filename, True, BLACK)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 8))
       

        pygame.draw.rect(screen, GREEN, save_button)
        pygame.draw.rect(screen, RED, cancel_button)

        screen.blit(FONT.render("Save", True, WHITE), (save_button.x + 25, save_button.y + 8))
        screen.blit(FONT.render("Cancel", True, WHITE), (cancel_button.x + 15, cancel_button.y + 8))

        msg_surface = FONT.render(message, True,"red")
        screen.blit(msg_surface, (560, 400))





    
# draw pieces onto board(150, 170, 200)
def draw_pieces():
    
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 102 + 22, white_locations[i][1] * 75+ 30))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 102+ 10, white_locations[i][1] * 75 + 10))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 75 + 1,
                                                    100, 75], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 102 + 22, black_locations[i][1] * 75 + 30))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 102 + 10, black_locations[i][1] * 75 + 10))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 75 + 1,
                                                    100, 75], 2)


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


# add pawn promotion
def check_promotion():
    pawn_indexes = []
    
    white_promotion = False
    black_promotion = False
    promote_index = 100
    for i in range(len(white_pieces)):
        if white_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if white_locations[pawn_indexes[i]][1] == 7:
            white_promotion = True
        
            promote_index = pawn_indexes[i]
    pawn_indexes = []
    for i in range(len(black_pieces)):
        if black_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if black_locations[pawn_indexes[i]][1] == 0:
            black_promotion = True
            

            promote_index = pawn_indexes[i]
    return white_promotion, black_promotion, promote_index


def draw_promotion():
    pygame.draw.rect(screen, desired_color_light, [800, 0, 200, 420])
    if white_promote:
        color = 'white'
        for i in range(len(white_promotions)):
            piece = white_promotions[i]
            index = piece_list.index(piece)
            screen.blit(white_images[index], (860, 5 + 100 * i))
    elif black_promote:
        color = 'black'
        for i in range(len(black_promotions)):
            piece = black_promotions[i]
            index = piece_list.index(piece)
            screen.blit(black_images[index], (860, 5 + 100 * i))
    pygame.draw.rect(screen,desired_color_dark, [800, 0, 200, 420], 8)


def check_promo_select():
    mouse_pos = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    x_pos = mouse_pos[0] // 100
    y_pos = mouse_pos[1] // 100
    
    if white_promote and left_click and x_pos > 7 and y_pos < 4:
        white_pieces[promo_index] = white_promotions[y_pos]
        
    elif black_promote and left_click and x_pos > 7 and y_pos < 4:
        black_pieces[promo_index] = black_promotions[y_pos]
    


# main game loop
draw_static_board(board_surface)
sound_oce=True
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True
while run:
    
    timer.tick(fps)

    if counter < 30:
        counter += 1
    else:
        counter = 0

    screen.fill(MAIN_BACKGROUND_COLOR)
    
    draw_board()
    if not want_to_save:
        draw_pieces()

        draw_captured()
        draw_check()
   
    if not game_over:
        white_promote, black_promote, promo_index = check_promotion()
        if white_promote or black_promote:
            draw_promotion()
            check_promo_select()
            
            
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
        if selected_piece == 'king':
            draw_castling(castling_moves)
    mouse_pos = pygame.mouse.get_pos()
    if mouse_pos[0] > 1072 and mouse_pos[1] > 258 and mouse_pos[0] < 1241 and mouse_pos[1] < 410 and not want_to_save :
        
        button_x= mouse_pos[0] -1075
        button_y= mouse_pos[1]-263
        button_coords=(button_x//160,button_y//75)
        if button_coords ==(0,0):
            pygame.draw.rect(screen,CONTAINER_BOX_BG, [1076,260, 160, 75],border_radius=20)
            pygame.draw.rect(screen,BUTTON_BACK_GROUND_BORDER, [1076,260, 160, 75],3,border_radius=20)
            screen.blit(Semimedium_font.render('SAVE', True,  TEXT_COLOR_FOR_HEADINGS), (1125, 286))
                

        elif button_coords ==(0,1):
            pygame.draw.rect(screen,CONTAINER_BOX_BG, [1076,340, 160, 75],border_radius=20)
            pygame.draw.rect(screen,BUTTON_BACK_GROUND_BORDER, [1076,340, 160, 75],3,border_radius=20)
            screen.blit(Semimedium_font.render('UNDO', True, TEXT_COLOR_FOR_HEADINGS), (1125, 366))
            
            


    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False



        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over and not want_to_save:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 75
            click_coords = (x_coord, y_coord)
            
            
            if turn_step <= 1:
                
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'black'
                if click_coords in white_locations:
                    generated_move=name_of_move('',x_coord, y_coord,True)
                    history_move_key=click_coords
                    selection = white_locations.index(click_coords)
                    # check what piece is selected, so you can only draw castling moves if king is selected
                    selected_piece = white_pieces[selection]
                    if turn_step == 0:
                        turn_step = 1
                if click_coords in valid_moves and selection != 100:
                    
                    white_ep = check_ep(white_locations[selection], click_coords)
                    white_locations[selection] = click_coords
                    white_moved[selection] = True
                    history_move_value=click_coords
                    history_of_move[history_move_key]=history_move_value


                    if click_coords in black_locations:
                        
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        his_white_material_score.append(white_material_score)
                        white_material_score = white_material_score    +  material_score(black_pieces[black_piece])
        
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                        black_moved.pop(black_piece)
                        sound.play("capture")
                    else:
                        sound.play("move")
                   
                    # adding check if en passant pawn was captured
                    if click_coords == black_ep:
                        black_piece = black_locations.index((black_ep[0], black_ep[1] - 1))
                        captured_pieces_white.append(black_pieces[black_piece])
                        sound.play("capture")

                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                        black_moved.pop(black_piece)
                        his_white_material_score.append(white_material_score)
                        white_material_score = white_material_score    +  material_score(black_pieces[black_piece])
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []
                    
                    generated_move=name_of_move(generated_move,x_coord, y_coord,True)
                    history_of_white_locs.append(white_locations.copy())
                    history_of_white_pieces.append(white_pieces.copy())
                    history_of_white_moved.append(white_moved.copy())
                    history_captured_pieces_white.append(captured_pieces_white.copy())

                    history_captured_pieces_black.append(captured_pieces_black.copy())
                    history_of_black_locs.append(black_locations.copy())
                    history_of_black_pieces.append(black_pieces.copy())
                    history_of_black_moved.append(white_moved.copy())
                    
                # add option to castle
                elif selection != 100 and selected_piece == 'king':
                    for q in range(len(castling_moves)):
                        if click_coords == castling_moves[q][0]:
                            white_locations[selection] = click_coords
                            white_moved[selection] = True
                            if click_coords == (1, 0):
                                rook_coords = (0, 0)
                            else:
                                rook_coords = (7, 0)
                            rook_index = white_locations.index(rook_coords)
                            white_locations[rook_index] = castling_moves[q][1]
                            black_options = check_options(black_pieces, black_locations, 'black')
                            white_options = check_options(white_pieces, white_locations, 'white')
                            turn_step = 2
                            selection = 100
                            valid_moves = []
                            sound.play("move")
                            generated_move=name_of_move(generated_move,x_coord, y_coord,True)
                            history_of_white_locs.append(white_locations.copy())
                            history_of_white_pieces.append(white_pieces.copy())
                            history_of_white_moved.append(white_moved.copy())
                            history_captured_pieces_white.append(captured_pieces_white.copy())

                            history_captured_pieces_black.append(captured_pieces_black.copy())
                            history_of_black_locs.append(black_locations.copy())
                            history_of_black_pieces.append(black_pieces.copy())
                            history_of_black_moved.append(white_moved.copy())
                    
            if turn_step > 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'white'
                if click_coords in black_locations:
                    generated_move=name_of_move('',x_coord, y_coord,False)
                    history_move_key=click_coords
                    selection = black_locations.index(click_coords)
                    
                    # check what piece is selected, so you can only draw castling moves if king is selected
                    selected_piece = black_pieces[selection]
                    if turn_step == 2:
                        turn_step = 3
                if click_coords in valid_moves and selection != 100:
                    history_move_value=click_coords
                    history_of_move[history_move_key]=history_move_value

                    black_ep = check_ep(black_locations[selection], click_coords)
                    black_locations[selection] = click_coords
                    black_moved[selection] = True
                    if click_coords in white_locations:
                        white_piece = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece])
                        his_black_material_score.append(black_material_score)
                        black_material_score = black_material_score    +  material_score(white_pieces[white_piece])
                        
                        if white_pieces[white_piece] == 'king':
                            winner = 'black'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                        white_moved.pop(white_piece)
                
                        sound.play("capture")
                    else:
                        sound.play("move")
                    if click_coords == white_ep:
                        white_piece = white_locations.index((white_ep[0], white_ep[1] + 1))
                        captured_pieces_black.append(white_pieces[white_piece])
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                        white_moved.pop(white_piece)
                        sound.play("capture")
                        his_black_material_score.append(black_material_score)
                        black_material_score = black_material_score    +  material_score(white_pieces[white_piece])
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
                    
                    
                    generated_move=name_of_move(generated_move,x_coord, y_coord,False)
                    history_of_white_locs.append(white_locations.copy())
                    history_of_white_pieces.append(white_pieces.copy())
                    history_of_white_moved.append(white_moved.copy())
                    history_captured_pieces_white.append(captured_pieces_white.copy())

                    history_captured_pieces_black.append(captured_pieces_black.copy())
                    history_of_black_locs.append(black_locations.copy())
                    history_of_black_pieces.append(black_pieces.copy())
                    history_of_black_moved.append(white_moved.copy())
                # add option to castle
                elif selection != 100 and selected_piece == 'king':
                    for q in range(len(castling_moves)):
                        if click_coords == castling_moves[q][0]:
                            black_locations[selection] = click_coords
                            black_moved[selection] = True
                            if click_coords == (1, 7):
                                rook_coords = (0, 7)
                            else:
                                rook_coords = (7, 7)
                            rook_index = black_locations.index(rook_coords)
                            black_locations[rook_index] = castling_moves[q][1]
                            black_options = check_options(black_pieces, black_locations, 'black')
                            white_options = check_options(white_pieces, white_locations, 'white')
                            turn_step = 0
                            selection = 100
                            valid_moves = []
                            sound.play("move")
                            generated_move=name_of_move(generated_move,x_coord, y_coord,False)
                            history_of_white_locs.append(white_locations.copy())
                            history_of_white_pieces.append(white_pieces.copy())
                            history_of_white_moved.append(white_moved.copy())
                            history_captured_pieces_white.append(captured_pieces_white.copy())

                            history_captured_pieces_black.append(captured_pieces_black.copy())
                            history_of_black_locs.append(black_locations.copy())
                            history_of_black_pieces.append(black_pieces.copy())
                            history_of_black_moved.append(white_moved.copy())
                
                            
            
            if x_coord in [11,12] and y_coord in[6,7]:
                color_x= event.pos[0] -1096
                color_y= event.pos[1]-481
                color_coords=(color_x//66,color_y//66)
            
                if color_coords in board_color_location:
                    board_color_index=board_color_location.index(color_coords)
                    desired_color_light=possible_board_color[board_color_index][0]
                    desired_color_dark=possible_board_color[board_color_index][1]
                    
                    #backgrounds
                    CAPTURED_BG = CAPTURED_BG_variations[board_color_index]

                    CONTAINER_BOX_BG = CONTAINER_BOX_BG_variations[board_color_index]
                    CONTAINER_BOX_BORDER  = CONTAINER_BOX_BORDER_variations[board_color_index]

                    CONTENT_CONTAINER_BG = CONTENT_CONTAINER_BG_variation[board_color_index]
                    CONTENT_CONTAINER_BG_BORDER = CONTENT_CONTAINER_BG_BORDER_variation[board_color_index]


                    MAIN_BACKGROUND_COLOR = MAIN_BACKGROUND_COLOR_variation[board_color_index]
                    MAIN_QUALITY_PANNEL_BG = MAIN_QUALITY_PANNEL_BG_variation[board_color_index]


                    TEXT_COLOR_FOR_HEADINGS = TEXT_COLOR_FOR_HEADINGS_variation[board_color_index]

                    BUTTON_BACK_GROUND_COLOR = BUTTON_BACK_GROUND_COLOR_variation[board_color_index]
                    BUTTON_BACK_GROUND_BORDER = BUTTON_BACK_GROUND_BORDER_variation[board_color_index]
                    DULL_TEXT=DULL_TEXT_COLOR_variation[board_color_index]
                    BUTTON_HOVER_COLOR = BUTTON_HOVER_COLOR_variatio[board_color_index]


                    draw_static_board(board_surface)

            print(event.pos)
        
            if x_coord in[10,11,12] and y_coord in [3,4,5] :
                button_x= event.pos[0] -1075
                button_y= event.pos[1]-263
                button_coords=(button_x//160,button_y//75)
                
                if button_coords ==(0,0):
                    pygame.draw.rect(screen,BUTTON_BACK_GROUND_COLOR , [1076,260, 160, 75],border_radius=20)
                  
                    want_to_save=True

                elif button_coords ==(0,1):
                    pygame.draw.rect(screen,BUTTON_BACK_GROUND_COLOR, [1076,340, 160, 75],border_radius=20)
                  
                    print("yes")
                    undo_the_move()

        #to save the textfile
        
        

        if event.type == pygame.MOUSEBUTTONDOWN and want_to_save:
            if input_box.collidepoint(event.pos):
                active = True
            else:
                active = False

            if save_button.collidepoint(event.pos):
                if filename:
                    text_to_save = "".join(history_everymove[-1])
                    print(text_to_save)
                    save_to_file(filename, text_to_save)
                    print("saved", filename)
                    pygame.time.delay(700)
                    want_to_save = False
                else:
                    message = "Enter file name!"

               


            if cancel_button.collidepoint(event.pos):
                want_to_save=False
                
        
        if event.type == pygame.KEYDOWN and active and want_to_save:
            if event.key == pygame.K_BACKSPACE:
                filename = filename[:-1]
            elif event.key == pygame.K_RETURN:
                print(filename)
                pygame.time.delay(700)
                want_to_save=False
            
            else:
                filename += event.unicode

        #ends here to save file text

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                run = False

    if winner != '':
        
        if sound_oce:
            sound.play("checkmate")
            sound_oce=False
        game_over = True
        draw_game_over()

    pygame.display.flip()
pygame.quit()
