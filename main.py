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
                # TODO handle player move
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