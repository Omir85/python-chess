import pygame
import board
import colors

class ChessBoard(board.Board):

    ASCII_FOR_LOWER_CASE_A = 97

    DARK_PLAYER = colors.BLACK_COLOR
    LIGHT_PLAYER = colors.WHITE_COLOR

    HIGHLIGHT_COLOR = colors.ORANGE_COLOR

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
    
    def from_fen(self, fen : str):
        fen_configuration = {}
        fens = fen.split(" ")
        position = fens[0]
        lines = position.split("/")
        current_row = 0
        current_file = 0
        for i, line in enumerate(lines):
            contents = [character for character in line]
            for piece in contents:
                if piece.isalnum():
                    if piece.isalpha():
                        square = self.get_file(current_file) + self.get_row(current_row)
                        fen_configuration[square] = piece
                        current_file, current_row = self.next_square(current_file, current_row)
                    else:
                        number_of_empty_squares = int(piece)
                        for _ in range(number_of_empty_squares):
                            current_file, current_row = self.next_square(current_file, current_row)
                else:
                    raise Exception(f"Unexpected fen content: {piece} in {contents}")
        return fen_configuration

    def get_row(self, row):
        return str(8 - row)

    def get_file(self, column):
        return chr(column + 97)

    def get_area(self, row, column):
        return (row * self.square_size, column * self.square_size, self.square_size, self.square_size)

    def get_color(self, square):
        if square == ChessBoard.DARK_SQUARE:
            return colors.GREY_COLOR
        return colors.WHITE_COLOR
    
    def draw_square(self, window, row, column, square):
        pygame.draw.rect(window, self.get_color(square), self.get_area(row, column))

    def highlight_square(self, window, row, column):
        pygame.draw.rect(window, self.HIGHLIGHT_COLOR, self.get_area(row, column), 3)

    def switch_color(self, square):
        if square == ChessBoard.LIGHT_SQUARE:
            return ChessBoard.DARK_SQUARE
        return ChessBoard.LIGHT_SQUARE
    
    def draw(self, window, legal_moves=[]):
        square = ChessBoard.LIGHT_SQUARE
        for row in range(self.rows):
            for column in range(self.columns):
                self.draw_square(window, row, column, square)
                square = self.switch_color(square)
            square = self.switch_color(square)
    
    def get_position_player(self, piece : str):
        if piece.islower():
            return self.DARK_PLAYER
        return self.LIGHT_PLAYER

    def get_positions(self, player_color):
        positions = []
        for position in self.configuration.items():
            piece = position[1]
            if piece is not None and self.get_position_player(piece) == player_color:
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
    
    def get_hightlight_square_coordinates(self, square):
        file = self.convert(square[0])
        row = 8 - int(square[1])
        coordinates = file * self.square_size, self.square_size * row
        return coordinates
    
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
        legal_moves.extend(self.get_pieces_attacked_by(square))
        # TODO handle special cases for king moves
        return legal_moves

    def get_board_coordinates(self, square):
        column, row = square[:]
        row = 8 - int(row)
        column = self.convert(column)
        return column, row

    def get_pieces_attacked_by(self, square:str) -> [str]:
        attacked_pieces = []
        piece = self.get_piece(square)
        column, row = self.get_board_coordinates(square)
        attackable_squares = []
        direction = -1 if piece.isupper() else 1
        if piece.lower() == "p":
            attack_directions = [(-1, direction), (1, direction)]
            attack_range = 1
        # TODO implement other pieces attack strategy
        for i in range(attack_range):
            for attack_direction in attack_directions:
                attackable_square = (column + attack_direction[0] * (i + 1), row + attack_direction[1] * (i + 1))
                attackable_squares.append(attackable_square)
        for attackable_square in attackable_squares:
            target_square = self.get_file(attackable_square[0]) + self.get_row(attackable_square[1])
            piece = self.get_piece(target_square)
            if piece is not None:
                attacked_pieces.append(target_square)
        return attacked_pieces

    def get_player_from_square(self, square):
        piece = self.get_piece(square)
        if piece == None:
            raise Exception(f"square {square} is empty")
        return self.LIGHT_PLAYER if piece.isupper() else self.DARK_PLAYER
    
    def get_legal_moves(self, piece, starting_square):
        legal_moves = []
        if piece == self.PAWN:
            legal_moves.extend(self.get_pawn_legal_moves(starting_square))
        return legal_moves

    def move(self, from_square, to_square):
        self.configuration[to_square] = self.configuration.get(from_square)
        self.configuration[from_square] = None

    def __str__(self) -> str:
        return self.configuration