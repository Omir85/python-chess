import pygame
import board
import colors

class ChessBoard(board.Board):

    ASCII_FOR_LOWER_CASE_A = 97

    DARK_PLAYER = colors.BLACK_COLOR
    LIGHT_PLAYER = colors.WHITE_COLOR

    players = [LIGHT_PLAYER, DARK_PLAYER]
    player_colors = [DARK_PLAYER, LIGHT_PLAYER]
    DARK_SQUARE = False
    LIGHT_SQUARE = True

    KING = "K"
    QUEEN = "Q"
    ROOK = "R"
    BISHOP = "B"
    KNIGHT = "N"
    PAWN = "P"

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
        # print(fen_configuration)
        # FIXME re-implement from_fen and remove hardcoded initialisation
        fen_configuration = {
            'a8' : 'r', 'b8' : 'n', 'c8' : 'b', 'd8' : 'q', 'e8' : 'k', 'f8' : 'b', 'g8' : 'n', 'h8' : 'r', 
            'a7' : 'p', 'b7' : 'p', 'c7' : 'p', 'd7' : 'p', 'e7' : 'p', 'f7' : 'p', 'g7' : 'p', 'h7' : 'p', 
            'a2' : 'P', 'b2' : 'P', 'c2' : 'P', 'd2' : 'P', 'e2' : 'P', 'f2' : 'P', 'g2' : 'P', 'h2' : 'P', 
            'a1' : 'R', 'b1' : 'N', 'c1' : 'B', 'd1' : 'Q', 'e1' : 'K', 'f1' : 'B', 'g1' : 'N', 'h1' : 'R'
        }
        return fen_configuration

    def get_row(self, row):
        return str(8 - row)

    def get_file(self, column):
        return chr(column + 97)

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
                # self.highlight_if_legal_move_square(row, column, square)
                square = self.switch_color(square)
            square = self.switch_color(square)
    
    def get_position_player(self, piece : str):
        if piece.islower():
            return self.DARK_PLAYER
        return self.LIGHT_PLAYER

    def get_positions(self, player_color):
        positions = []
        for position in self.configuration.items():
            if self.get_position_player(position[1]) == player_color:
                positions.append(position)
        return positions

    def get_piece_color(self, piece:str, player):
        pieces = self.DARK_PIECES
        if player == self.players[0]:
            pieces = self.LIGHT_PIECES
        return pieces[piece.upper()]
    
    def place_pieces(self, window):
        for player in self.players:
            for square, piece in self.get_positions(player):
                piece_sprite = self.get_piece_color(piece, player)
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
        piece = self.configuration.get(square)
        return piece is not None and player == self.get_position_player(piece)

    def get_piece(self, square):
        return self.configuration.get(square)

    def get_pawn_legal_moves(self, square:str):
        legal_moves = []
        file = square[0]
        row = int(square[1])
        player = self.get_player_from_square(square)
        is_white_player = player == self.LIGHT_PLAYER
        is_white_starting_position = row == 2 and is_white_player
        is_black_starting_position = row == 7 and not is_white_player
        direction = 1 if is_white_player else -1
        if is_white_starting_position or is_black_starting_position:
            legal_moves.append(f"{file}{row+2*direction}")
        legal_moves.append(f"{file}{row+1*direction}")
        illegal_moves = []
        for move in legal_moves:
            if self.configuration.get(move) is not None:
                illegal_moves.append(move)
        for move in illegal_moves:
            legal_moves.remove(move)
        return legal_moves

    def get_player_from_square(self, square):
        piece = self.get_piece(square)
        if piece == None:
            raise Exception(f"square {square} is empty")
        return self.LIGHT_PLAYER if piece.isupper() else self.DARK_PLAYER
    
    def get_legal_moves(self, piece, starting_square):
        legal_moves = []
        # player = self.get_player_from_square(starting_square)
        if piece == self.PAWN:
            legal_moves.extend(self.get_pawn_legal_moves(starting_square))
        return legal_moves

    def __str__(self) -> str:
        return self.configuration