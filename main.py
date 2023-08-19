import pygame
from ui import create_window
from graphics import draw_text, clear_window, redraw_window
import colors
import chessboard

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

players = chessboard.ChessBoard.players
current_player = starting_player = players[0]

'''
Chess game

Board : 8x8 square
Token : Piece | Pawn
Piece : Rook | Knight | Bishop | Queen | King
'''

def should_exit(event):
    if event.type == pygame.QUIT:
        return True
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
            return True

def is_click(event):
    return event.type == pygame.MOUSEBUTTONUP

def get_clicked_square(board, position):
    file, row = position
    f = board.get_file(int(file/board.square_size))
    r = board.get_row(int(row/board.square_size))
    clicked_square = f"{f}{r}"
    return clicked_square

def did_click_on_player_piece(window, square):
    pass

def get_clicked_player_piece(window, square):
    pass

def show_legal_moves(window, piece, square):
    pass

def hide_legal_moves():
    pass

def is_legal_move(window, piece, square):
    pass

def move(window, piece, square):
    pass

def next_player(player):
    if player == players[0]:
        return players[1]
    return players[0]

def start_game(window):
    run = True
    board = chessboard.ChessBoard(WINDOW_WIDTH/8)
    piece_selected = None
    while run:
        for event in pygame.event.get():
            if should_exit(event):
                print("stopping game")
                run = False
            else:
                # TODO handle player side switch
                # TODO handle player move
                if is_click(event):
                    square = get_clicked_square(board, pygame.mouse.get_pos())
                    if piece_selected == None:
                        # the player did not have a piece selected
                        if did_click_on_player_piece(window, square):
                            piece_selected = get_clicked_player_piece(window, square)
                            show_legal_moves(window, piece_selected, square)
                    else:
                        # the player did have a piece selected and now wants to move the piece somewhere else
                        if is_legal_move(piece_selected, square):
                            # TODO move the piece if legal move
                            move(window, piece_selected, square)
                            # TODO apply taking rules
                            # TODO handle check / checkmate / stalemate
                            # TODO switch active player if legal move made
                            piece_selected = None
                            current_player = next_player(current_player)
                        else:
                            # keep piece selected if illegal move
                            pass
                        if did_click_on_player_piece(window, square):
                            second_piece_selected = get_clicked_player_piece(window, square)
                            if second_piece_selected == piece_selected:
                                hide_legal_moves()
                                piece_selected = None
                clear_window(window)
                board.draw(window)
                board.place_pieces(window)
                redraw_window()

def main():
    window = create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Chess")
    # TODO display welcome menu
    run = True
    while run:
        clear_window(window)
        draw_text(window, "Press q to quit or any other key to start a game", 20, colors.BLUE_COLOR, 50, 100)
        redraw_window()
        for event in pygame.event.get():
            if should_exit(event):
                print("quitting...")
                run = False
            elif event.type == pygame.KEYDOWN:
                start_game(window)

if __name__ == "__main__":
    pygame.font.init()
    main()