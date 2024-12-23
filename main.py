import pygame
from ui import create_window
from graphics import draw_text, clear_window, redraw_window
import colors
import chessboard

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

players = chessboard.ChessBoard.players
current_player = players[0]

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

def highlight_squares(window, board:chessboard.ChessBoard, squares):
    for square in squares:
        coordinates = board.get_highlight_square_coordinates(square)
        board.highlight_square(window, coordinates[0] / board.square_size, coordinates[1] / board.square_size)

def highlight_king_square(window, board:chessboard.ChessBoard, square, status):
    # on check status, color square in yellow
    if status == "CHECK":
        color = board.CHECK_COLOR
        print(f"Marking square {square} in {color}")
        coordinates = board.get_highlight_square_coordinates(square)
        board.highlight_square(window, coordinates[0] / board.square_size, coordinates[1] / board.square_size, color)
    elif status == "CHECKMATE":
        # on checkmate status, color square in red
        color = board.CHECKMATE_COLOR
        print(f"Marking square {square} in {color}")
        coordinates = board.get_highlight_square_coordinates(square)
        board.highlight_square(window, coordinates[0] / board.square_size, coordinates[1] / board.square_size, color)
    else:
        # unknown status
        print(f"Status unknown: {status}")

def start_game(window):
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
            elif should_take_fen_snapshot(event):
                print("taking fen snapshot")
                fen_snapshot = take_fen_snapshot(board)
                # does not print until game is stopped
                print(f"{fen_snapshot}")
            else:
                if is_click(event):
                    square = board.get_clicked_square(pygame.mouse.get_pos())
                    highlight_squares(window, board, [square])
                    if piece_selected == None:
                        # the player did not have a piece selected
                        if board.did_click_on_player_piece(square):
                            piece_selected = board.get_piece(square)
                            square_selected = square
                            legal_moves = board.get_legal_moves(piece_selected, square)
                            from_square = square
                        else:
                            pass
                    else:
                        # the player did have a piece selected and now wants to move the piece somewhere else
                        if square in legal_moves:
                            if current_player == board.LIGHT_PLAYER:
                                board.white_en_passant_target_file = None
                            else:
                                board.black_en_passant_target_file = None
                            board.move(from_square, square)
                            from_square = None
                            legal_moves = []
                            piece_selected = None
                            square_selected = None
                            board.switch_player()
                        else:
                            # player selects another piece
                            if board.did_click_on_player_piece(square):
                                piece_selected = board.get_piece(square)
                                square_selected = square
                                legal_moves = board.get_legal_moves(piece_selected, square)
                                from_square = square
                            else:
                            # unselect if same piece clicked twice
                                legal_moves = []
                                piece_selected = None
                                square_selected = None
        clear_window(window)
        board.draw(window, legal_moves)
        board.place_pieces(window)
        highlight_squares(window, board, legal_moves)
        
        # MANUAL TEST
        # square = "e1"
        # status = "CHECK"
        # highlight_king_square(window, board, square, status)
        # square = "e8"
        # status = "CHECKMATE"
        # highlight_king_square(window, board, square, status)

        redraw_window()

def should_take_fen_snapshot(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_p:
            return True
    return False

def take_fen_snapshot(board):
    return board.to_fen()

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