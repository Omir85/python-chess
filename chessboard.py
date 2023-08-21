import pygame
import board
import colors

class ChessBoard(board.Board):

    ASCII_FOR_LOWER_CASE_A = 97

    DARK_PLAYER = "Dark"
    LIGHT_PLAYER = "Light"

    players = [colors.WHITE_COLOR, colors.BLACK_COLOR]
    player_colors = [DARK_PLAYER, LIGHT_PLAYER]
    players2 = {LIGHT_PLAYER : colors.WHITE_COLOR, DARK_PLAYER : colors.BLACK_COLOR}
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
            self.DARK_PLAYER : {},
            self.LIGHT_PLAYER : {}
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
                        player_color = self.DARK_PLAYER if content.islower() else self.LIGHT_PLAYER
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

    def get_row(self, row):
        return str(8 - row)

    def get_file(self, column):
        return chr(column + 97)

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
    
    def draw(self, window, legal_moves=[]):
        square = ChessBoard.LIGHT_SQUARE
        for row in range(self.rows):
            for column in range(self.columns):
                self.draw_square(window, row, column, square)
                self.highlight_if_legal_move_square(row, column, square)
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
        if player_color == self.LIGHT_PLAYER:
            pieces = self.LIGHT_PIECES
        return pieces[piece]
    
    def place_pieces(self, window):
        for player_color in self.player_colors:
            for square, piece in self.get_positions(player_color):
                piece_sprite = self.get_piece(piece, player_color)
                coordinates = self.get_square_coordinates(square)
                
                self.draw_piece(window, piece_sprite, coordinates)
    
    def convert(self, file : str):
        return ord(file) - self.ASCII_FOR_LOWER_CASE_A
    
    def get_square_coordinates(self, square):
        file = self.convert(square[0])
        row = 8 - int(square[1])
        coordinates = file * self.square_size, self.square_size * row - 20
        return coordinates

    def draw_piece(self, window, piece, coordinates):
        font = pygame.font.SysFont("segoeuisymbol", int(self.square_size))
        label = font.render(piece, 1, colors.BLACK_COLOR)
        window.blit(label, coordinates)

    def get_clicked_square(self, position):
        file, row = position
        f = self.get_file(int(file/self.square_size))
        r = self.get_row(int(row/self.square_size))
        clicked_square = f"{f}{r}"
        return clicked_square
    
    def get_player(self, player):
        return self.LIGHT_PLAYER if player == colors.WHITE_COLOR else self.DARK_PLAYER
    
    def did_click_on_player_piece(self, player, square) -> bool:
        return self.configuration.get(self.get_player(player)).get(square) is not None

    def get_clicked_player_piece(self, square):
        for player in self.configuration:
            positions = self.configuration.get(player)
            for position in positions:
                piece = positions.get(position)
                if position == square:
                    return piece
        raise Exception(f"No piece found on {square}")

    def get_pawn_legal_moves(self, square:str):
        legal_moves = []
        file = square[0]
        row = int(square[1])
        player = self.get_player_from_square(square)
        is_white_player = player == self.LIGHT_PLAYER
        is_white_starting_position = row == 2 and is_white_player
        is_black_starting_position = row == 7 and not is_white_player
        direction = 1 if is_white_player else -1
        # TODO handle when pawn is stuck by another piece (own or opponent's)
        if is_white_starting_position or is_black_starting_position:
            legal_moves.append(f"{file}{row+2*direction}")
        legal_moves.append(f"{file}{row+1*direction}")
        return legal_moves

    def get_player_from_square(self, square):
        player = None
        for player in self.configuration:
            positions = self.configuration.get(player)
            if square in positions.keys():
                return player
        raise Exception(f"square {square} is empty")
    
    def get_legal_moves(self, piece, starting_square):
        legal_moves = []
        player = self.get_player_from_square(starting_square)
        if piece == self.PAWN:
            legal_moves.extend(self.get_pawn_legal_moves(starting_square))
        return legal_moves

    def __str__(self) -> str:
        string = ""
        for key in self.configuration.keys():
            string += key + ":"
            values = self.configuration.get(key)
            for value in values:
                string += "(" + value + ":" + values.get(value) + ")"
            string += "\n"
        return string.strip()