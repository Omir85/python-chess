import pygame
from chess import board
import colors

class ChessBoard(board.Board):

    ASCII_FOR_LOWER_CASE_A = 97

    DARK_PLAYER_COLOR = "Dark"
    LIGHT_PLAYER_COLOR = "Light"

    DARK_SQUARE = False
    LIGHT_SQUARE = True

    KING = "K"
    QUEEN = "Q"
    ROOK = "R"
    BISHOP = "B"
    KNIGHT = "N"
    PAWN = "p"

    PIECES = [KING, QUEEN, ROOK, BISHOP, KNIGHT, PAWN]

    DARK_PIECES = {
        KING : "♚",
        QUEEN : "♛",
        ROOK : "♜",
        BISHOP : "♝",
        KNIGHT : "♞",
        PAWN : "♟"
    }
    LIGHT_PIECES = {
        KING : "♔",
        QUEEN : "♕",
        ROOK : "♖",
        BISHOP : "♗",
        KNIGHT : "♘",
        PAWN : "♙"
    }

    def __init__(self, square_size, configuration=None) -> None:
        board.Board.__init__(self, 8, 8, square_size)
        self.players = [colors.WHITE_COLOR, colors.BLACK_COLOR]
        if configuration:
            self.configuration = configuration
        else:
            self.configuration = {
                self.LIGHT_PLAYER_COLOR : {
                    "a1" : self.ROOK, "a2" : self.KNIGHT, "a3" : self.BISHOP, "a4" : self.QUEEN, "a5" : self.KING, "a6" : self.BISHOP, "a7" : self.KNIGHT, "a8" : self.ROOK,
                    "b1" : self.PAWN, "b2" : self.PAWN, "b3" : self.PAWN, "b4" : self.PAWN, "b5" : self.PAWN, "b6" : self.PAWN, "b7" : self.PAWN, "b8" : self.PAWN,
                },
                "Dark" : {
                    "g1" : self.PAWN, "g2" : self.PAWN, "g3" : self.PAWN, "g4" : self.PAWN, "g5" : self.PAWN, "g6" : self.PAWN, "g7" : self.PAWN, "g8" : self.PAWN,
                    "h1" : self.ROOK, "h2" : self.KNIGHT, "h3" : self.BISHOP, "h4" : self.QUEEN, "h5" : self.KING, "h6" : self.BISHOP, "h7" : self.KNIGHT, "h8" : self.ROOK
                }
            }

    def get_row(self, line):
        return chr(line + 97)

    def get_file(self, column):
        return str(column + 1)

    def convert(self, line, column):
        row = self.get_row(line)
        file = self.get_file(column)
        return self.configuration.get(row + file, " ")

    def get_area(self, row, column):
        return (row * self.square_size, column * self.square_size, (row + 1) * self.square_size, (column + 1) * self.square_size)

    def get_color(self, square):
        if square == ChessBoard.DARK_SQUARE:
            return colors.GREY_COLOR
        return colors.WHITE_COLOR
    
    def draw_square(self, window, row, column, square):
        pygame.draw.rect(window, self.get_color(square), self.get_area(row, column), 0)

    def switch_color(self, square):
        if square == ChessBoard.LIGHT_SQUARE:
            return ChessBoard.DARK_SQUARE
        return ChessBoard.LIGHT_SQUARE
    
    def draw(self, window):
        square = ChessBoard.LIGHT_SQUARE
        for row in range(self.rows):
            for column in range(self.columns):
                self.draw_square(window, row, column, square)
                square = self.switch_color(square)
            square = self.switch_color(square)
    
    def get_positions(self, player_color):
        positions = []
        for player_position in self.configuration.items():
            if player_position[0] == player_color:
                for position in player_position[1].items():
                    positions.append(position)
        return positions
    
    def place_player_pieces(self, window, player_color):
        positions = self.get_positions(player_color)
        for square, piece in positions:
            coordinates = self.get_square_coordinates(square)
            self.draw_piece(window, self.get_piece(piece, player_color), coordinates, player_color)

    def get_piece(self, piece, player_color):
        pieces = self.DARK_PIECES
        if player_color == self.LIGHT_PLAYER_COLOR:
            pieces = self.LIGHT_PIECES
        return pieces[piece]
    
    def place_pieces(self, window):
        self.place_player_pieces(window, self.LIGHT_PLAYER_COLOR)
        self.place_player_pieces(window, self.DARK_PLAYER_COLOR)
    
    def convert(self, file : str):
        return ord(file) - self.ASCII_FOR_LOWER_CASE_A
    
    def get_square_coordinates(self, square):
        file = self.convert(square[0])
        row = int(square[1]) - 1

        return row * self.square_size, file * self.square_size - 20

    def get_piece_color(self, player_color):
        if player_color == self.LIGHT_PLAYER_COLOR:
            return colors.YELLOW_COLOR
        return colors.BROWN_COLOR

    def draw_piece(self, window, piece, coordinates, player_color):
        piece_color = self.get_piece_color(player_color)
        font = pygame.font.SysFont("segoeuisymbol", int(self.square_size))
        label = font.render(piece, 1, piece_color)
        window.blit(label, coordinates)