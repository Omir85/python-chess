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

# def highlight_square(window, board:chessboard.ChessBoard, square):
#     coordinates = board.get_hightlight_square_coordinates(square)
#     print(coordinates)
#     pass

def highlight_legal_moves(window, board:chessboard.ChessBoard, legal_moves):
    for square in legal_moves:
        coordinates = board.get_hightlight_square_coordinates(square)
        # print(coordinates)
        # highlight_square(window, board, square)
        board.highlight_square(window, coordinates[0] / board.square_size, coordinates[1] / board.square_size)

def hide_legal_moves():
    pass

def is_legal_move(piece, square):
    return True

def move(piece, square):

    pass

def next_player(player):
    if player == players[0]:
        return players[1]
    return players[0]

def start_game(window):
    global current_player
    legal_moves = []
    run = True
    board = chessboard.ChessBoard(WINDOW_WIDTH/8)
    piece_selected = None
    square_selected = None
    from_square = None
    while run:
        for event in pygame.event.get():
            if should_exit(event):
                print("stopping game")
                run = False
            else:
                # TODO handle player side switch
                # TODO handle player move
                if is_click(event):
                    square = board.get_clicked_square(pygame.mouse.get_pos())
                    if piece_selected == None:
                        # the player did not have a piece selected
                        if board.did_click_on_player_piece(current_player, square):
                            piece_selected = board.get_piece(square)
                            square_selected = square
                            legal_moves = board.get_legal_moves(piece_selected, square)
                            from_square = square
                    else:
                        # the player did have a piece selected and now wants to move the piece somewhere else
                        if is_legal_move(piece_selected, square):
                            # TODO move the piece if legal move
                            board.move(from_square, square)
                            from_square = None
                            legal_moves = []
                            # TODO apply taking rules
                            # TODO handle check / checkmate / stalemate
                            piece_selected = None
                            square_selected = None
                            current_player = next_player(current_player)
                        else:
                            # keep piece selected if illegal move
                            pass
                        # unselect if same piece clicked twice
                        if board.did_click_on_player_piece(current_player, square):
                            if square == square_selected:
                                legal_moves = []
                                piece_selected = None
                                square_selected = None
        clear_window(window)
        board.draw(window, legal_moves)
        board.place_pieces(window)
        highlight_legal_moves(window, board, legal_moves)
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