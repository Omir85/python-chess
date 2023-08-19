import pygame
from chess import board
import colors

class ChessBoard(board.Board):

    ASCII_FOR_LOWER_CASE_A = 97

    DARK_PLAYER_COLOR = "Dark"
    LIGHT_PLAYER_COLOR = "Light"

    players = [colors.BLACK_COLOR, colors.WHITE_COLOR]
    player_colors = [DARK_PLAYER_COLOR, LIGHT_PLAYER_COLOR]

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

    __STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def __init__(self, square_size, fen=None) -> None:
        board.Board.__init__(self, 8, 8, square_size)
        if not fen:
            fen = self.__STARTING_FEN
        self.configuration = self.from_fen(fen)

    def next_square(self, file, row):
        file += 1
        if file == 8:
            file = 0
            row += 1
        return file, row
    
    def get_fen_piece(self, piece : str):
        if piece.lower() == "r":
            return self.ROOK
        if piece.lower() == "n":
            return self.KNIGHT
        if piece.lower() == "b":
            return self.BISHOP
        if piece.lower() == "q":
            return self.QUEEN
        if piece.lower() == "k":
            return self.KING
        if piece.lower() == "p":
            return self.PAWN
        else:
            raise Exception(f"Unexpected piece : {piece}")
    
    def from_fen(self, fen : str):
        fen_configuration = {
            self.DARK_PLAYER_COLOR : {},
            self.LIGHT_PLAYER_COLOR : {}
        }
        fens = fen.split(" ")
        position = fens[0]
        lines = position.split("/")
        current_row = 0
        current_file = 0
        for i, line in enumerate(lines):
            contents = [character for character in line]
            for content in contents:
                if content.isalnum():
                    if content.isalpha():
                        square = self.get_file(current_file) + self.get_row(current_row)
                        player_color = self.DARK_PLAYER_COLOR if content.islower() else self.LIGHT_PLAYER_COLOR
                        piece = self.get_fen_piece(content)
                        if fen_configuration[player_color] == None:
                            fen_configuration[player_color] = {}
                        fen_configuration[player_color][square] = piece
                        current_file, current_row = self.next_square(current_file, current_row)
                    else:
                        number_of_empty_squares = int(content)
                        for _ in range(number_of_empty_squares):
                            current_file, current_row = self.next_square(current_file, current_row)
                else:
                    raise Exception(f"Unexpected fen content: {content} in {contents}")
        return fen_configuration

    def get_row(self, column):
        return str(column + 1)

    def get_file(self, line):
        return chr(8 - line + 96)

    def to_square(self, line, column):
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

    def get_piece(self, piece, player_color):
        pieces = self.DARK_PIECES
        if player_color == self.LIGHT_PLAYER_COLOR:
            pieces = self.LIGHT_PIECES
        return pieces[piece]
    
    def place_pieces(self, window):
        for player_color in self.player_colors:
            for square, piece in self.get_positions(player_color):
                piece_sprite = self.get_piece(piece, player_color)
                coordinates = self.get_square_coordinates(square)
                
                self.draw_piece(window, piece_sprite, coordinates, player_color)
    
    def convert(self, file : str):
        return ord(file) - self.ASCII_FOR_LOWER_CASE_A
    
    def get_square_coordinates(self, square):
        file = 8 - self.convert(square[0]) - 1
        row = int(square[1]) - 1
        coordinates = file * self.square_size, self.square_size * row - 20
        return coordinates

    def get_piece_color(self, player_color):
        if player_color == self.LIGHT_PLAYER_COLOR:
            return colors.YELLOW_COLOR
        return colors.BROWN_COLOR

    def draw_piece(self, window, piece, coordinates, player_color):
        piece_color = self.get_piece_color(player_color)
        font = pygame.font.SysFont("segoeuisymbol", int(self.square_size))
        label = font.render(piece, 1, piece_color)
        window.blit(label, coordinates)

    def __str__(self) -> str:
        string = ""
        for key in self.configuration.keys():
            string += key + ":"
            values = self.configuration.get(key)
            for value in values:
                string += "(" + value + ":" + values.get(value) + ")"
            string += "\n"
        return string.strip()