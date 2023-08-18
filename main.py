import pygame
from ui import create_window
from graphics import draw_text, clear_window, redraw_window
import colors
from chess import chessboard

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

'''
Chess game

Board : 8x8 square
Token : Piece | Pawn
Piece : Rook | Knight | Bishop | Queen | King

Piece can move, take when moving
Check when king is attacked
Checkmate when Check and King has no legal move
Stalemate when opponent has no legal move

Phase 1: Board is displayed with rows and files
Phase 2: Pieces are on the board
Phase 2.5: Implement chess notation to quickload a board
Phase 3: Pieces can move
Phase 4: Pieces can take
Phase 5: Check
Phase 6: Stalemate
Phase 7: Checkmate
Phase 8: Promotion
Phase 9: En passant
Phase 10: Implement time

'''

def should_exit(event):
    if event.type == pygame.QUIT:
        return True
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
            return True

def start_game(window):
    run = True
    board = chessboard.ChessBoard(WINDOW_WIDTH/8)
    while run:
        for event in pygame.event.get():
            if should_exit(event):
                print("stopping game")
                run = False
            else:
                clear_window(window)
                board.draw(window)
                # place pieces
                board.place_pieces(window)
                redraw_window()

def main():
    window = create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Chess")
    # display welcome menu
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