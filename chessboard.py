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

    __DEFAULT_FEN_END = " w KQkq - 0 1"
    __STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR" + __DEFAULT_FEN_END

    def __init__(self, square_size, fen=None) -> None:
        board.Board.__init__(self, 8, 8, square_size)
        if not fen:
            fen = self.__STARTING_FEN
        self.configuration = self.from_fen(fen)
        self.current_player = self.LIGHT_PLAYER
        self.has_white_king_moved = False
        self.has_black_king_moved = False
        self.has_white_short_castle_rook_moved = False
        self.has_white_long_castle_rook_moved = False
        self.has_black_short_castle_rook_moved = False
        self.has_black_long_castle_rook_moved = False

    def get_default_fen_end(self):
        return self.__DEFAULT_FEN_END
    
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
        return chr(column + ChessBoard.ASCII_FOR_LOWER_CASE_A)

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
    
    def convert(self, file : str) -> int:
        return ord(file) - ChessBoard.ASCII_FOR_LOWER_CASE_A
    
    def get_hightlight_square_coordinates(self, square):
        file, row = self.from_square(square)
        coordinates = file * self.square_size, self.square_size * row
        return coordinates
    
    def get_square_coordinates(self, square):
        file, row = self.from_square(square)
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
    
    def did_click_on_player_piece(self, square) -> bool:
        piece = self.configuration.get(square)
        return piece is not None and self.current_player == self.get_position_player(piece)

    def get_piece(self, square):
        return self.configuration.get(square)

    def get_other_player(self, player):
        if player == self.players[0]:
            return self.players[1]
        return self.players[0]
    
    def is_pawn_stuck(self, square:str) -> bool:
        next_row = int(square[1]) + self.get_direction(square)
        forward_square = square[0] + str(next_row)
        if self.configuration.get(forward_square) is None:
            return False
        return self.get_player_from_square(forward_square) == self.get_other_player(self.current_player)

    def is_light_player(self, square):
        return self.get_player_from_square(square) == self.LIGHT_PLAYER

    def get_direction(self, square):
        return 1 if self.is_light_player(square) else -1

    def get_pawn_legal_moves(self, square:str):
        legal_moves = []
        file = square[0]
        row = int(square[1])
        is_white_player = self.is_light_player(square)
        is_white_starting_position = row == 2 and is_white_player
        is_black_starting_position = row == 7 and not is_white_player
        direction = self.get_direction(square)
        if not self.is_pawn_stuck(square):
            if is_white_starting_position or is_black_starting_position:
                legal_moves.append(f"{file}{row+2*direction}")
            if 0 < row+1*direction <= 8:
                legal_moves.append(f"{file}{row+1*direction}")
        illegal_moves = []
        for move in legal_moves:
            if self.configuration.get(move) is not None:
                illegal_moves.append(move)
        for move in illegal_moves:
            legal_moves.remove(move)
        legal_moves.extend(self.get_pieces_attacked_by(square))
        return legal_moves

    def get_moves(self, square, direction_x, direction_y):
        legal_moves = []
        for _ in range(2):
            direction_x *= -1
            for _ in range(2):
                direction_y *= -1
                squares_ahead = self.get_squares_ahead(square, direction_x, direction_y)
                # if square == "b7" and direction_x == 0 and direction_y == 1:
                #     print("squares ahead " + str(direction_x) + ":" + str(direction_y))
                #     print(squares_ahead)
                for square_ahead in squares_ahead:
                    if square_ahead not in legal_moves:
                        legal_moves.append(square_ahead)
        return legal_moves

    def get_bishop_legal_moves(self, square:str):
        return self.get_moves(square, -1, 1)

    def get_knight_moves(self, square, file_move, row_move):
        legal_moves = []
        for _ in range(2):
            for _ in range(2):
                column, line = self.from_square(square)
                if 0 <= line + row_move < 8:
                    target_square = self.to_square(column + file_move, line + row_move)
                    if self.is_on_board(target_square):
                        legal_moves.append(target_square)
                row_move *= -1
                if row_move > 0:
                    file_move *= -1
        return legal_moves
    
    def get_knight_legal_moves(self, square:str):
        moves = []
        moves.extend(self.get_knight_moves(square, 2, 1))
        moves.extend(self.get_knight_moves(square, 1, 2))
        legal_moves = []
        for move in moves:
            if self.configuration.get(move) is None or self.get_player_from_square(move) != self.current_player:
                legal_moves.append(move)
        return legal_moves

    def get_rook_legal_moves(self, square:str):
        legal_moves = self.get_moves(square, 0, 1)
        # if square == "b7":
        #     print("rook b7 vertical legal moves")
        #     print(legal_moves)
        legal_moves.extend(self.get_moves(square, 1, 0))
        # if square == "b7":
        #     print("rook b7 horizontal legal moves")
        #     print(self.get_moves(square, 1, 0))
        # if square == "b7":
        #     print("rook b7 all legal moves")
        #     print(legal_moves)
        return legal_moves

    def get_queen_legal_moves(self, square:str):
        legal_moves = self.get_bishop_legal_moves(square)
        legal_moves.extend(self.get_rook_legal_moves(square))
        return legal_moves

    def get_attackers(self, square:str):
        possible_attackers = []
        possible_attackers.extend(self.get_squares_ahead(square, -1, -1))
        possible_attackers.extend(self.get_squares_ahead(square, -1, 0))
        possible_attackers.extend(self.get_squares_ahead(square, -1, 1))
        possible_attackers.extend(self.get_squares_ahead(square, 0, -1))
        possible_attackers.extend(self.get_squares_ahead(square, 0, 1))
        possible_attackers.extend(self.get_squares_ahead(square, 1, -1))
        possible_attackers.extend(self.get_squares_ahead(square, 1, 0))
        possible_attackers.extend(self.get_squares_ahead(square, 1, 1))
        # if square == "a8":
        #     print(possible_attackers)
        attackers = []
        for possible_attacker in possible_attackers:
            if self.get_piece(possible_attacker) is not None and self.get_player_from_square(possible_attacker) != self.current_player:
                legal_moves = self.get_legal_moves(self.get_piece(possible_attacker), possible_attacker)
                if square in legal_moves:
                    attackers.append(possible_attacker)
        return attackers
    
    def is_attacked(self, square:str) -> bool:
        # if square == "b8":
        #     print("attackers")
        #     print(self.get_attackers(square))
        return len(self.get_attackers(square)) > 0
    
    def get_king_legal_moves(self, king_square:str):
        moves = []
        moves.extend(self.get_squares_ahead(king_square, -1, 1, limit=1))
        moves.extend(self.get_squares_ahead(king_square, -1, 0, limit=1))
        moves.extend(self.get_squares_ahead(king_square, -1, -1, limit=1))
        moves.extend(self.get_squares_ahead(king_square, 0, -1, limit=1))
        moves.extend(self.get_squares_ahead(king_square, 0, 1, limit=1))
        moves.extend(self.get_squares_ahead(king_square, 1, -1, limit=1))
        moves.extend(self.get_squares_ahead(king_square, 1, 0, limit=1))
        moves.extend(self.get_squares_ahead(king_square, 1, 1, limit=1))
        possible_moves = []
        for move in moves:
            if self.configuration.get(move) is None or self.get_player_from_square(move) != self.current_player:
                possible_moves.append(move)
        legal_moves = []
        king = self.get_piece(king_square)
        if len(possible_moves) > 0:
            for possible_move in possible_moves:
                piece = self.get_piece(possible_move)
                self.move(king_square, possible_move)
                if not self.is_attacked(possible_move):
                    legal_moves.append(possible_move)
                self.move(possible_move, king_square)
                self.configuration[possible_move] = piece
            self.configuration[king_square] = king
        return legal_moves

    def get_short_castle_move(self, square):
        if self.has_white_king_moved or self.has_white_short_castle_rook_moved:
            return []
        if self.current_player == self.LIGHT_PLAYER:
            squares_to_check_if_empty = ["f1", "g1"]
        else:
            squares_to_check_if_empty = ["f8", "g8"]
        for square_to_check in squares_to_check_if_empty:
            if self.configuration.get(square_to_check) != None:
                return []
            if self.is_attacked(square_to_check):
                return []
        if self.current_player == self.LIGHT_PLAYER:
            return ["g1"]
        else:
            return ["g8"]
    
    def get_long_castle_move(self, square):
        if self.has_white_king_moved or self.has_white_long_castle_rook_moved:
            return []
        if self.current_player == self.LIGHT_PLAYER:
            squares_to_check_if_empty = ["b1", "c1", "d1"]
        else:
            squares_to_check_if_empty = ["b8", "c8", "d8"]
        for square_to_check in squares_to_check_if_empty:
            if self.configuration.get(square_to_check) != None:
                return []
            if self.is_attacked(square_to_check):
                return []
        if self.current_player == self.LIGHT_PLAYER:
            return ["c1"]
        else:
            return ["c8"]
    
    def from_square(self, square:str):
        column = self.convert(square[0])
        line = 8 - int(square[1])
        return column, line
    
    def to_square(self, column, line):
        file = self.get_file(column)
        row = self.get_row(line)
        square = f"{file}{row}"
        return square
    
    def is_on_board(self, square):
        column, line = self.from_square(square)
        # if square == "b8":
        #     print("is on board ?")
        #     print(column, line)
        #     print(0 <= column < 8 and 0 <= line < 8)
        return 0 <= column < 8 and 0 <= line < 8

    def get_squares_ahead(self, square, direction_x, direction_y, limit = None):
        squares_ahead = []
        column, line = self.from_square(square)
        # if square == "b7" and direction_x == 0 and direction_y == 1:
        #         print("init column line")
        #         print(column, line)
        while True:
            column += direction_x
            line -= direction_y
            square_ahead = self.to_square(column, line)
            # if square == "b7" and direction_x == 0 and direction_y == 1:
            #     print("column line")
            #     print(column, line)
            #     print(square_ahead)
            if not self.is_on_board(square_ahead):
                break
            if self.configuration.get(square_ahead) is None:
                # if square == "b7" and direction_x == 0 and direction_y == 1:
                #     print("asd " + square_ahead)
                squares_ahead.append(square_ahead)
            else:
                # if square == "b7" and direction_x == 0 and direction_y == 1:
                #     print("here now")
                squares_ahead_player = self.get_player_from_square(square_ahead)
                piece = self.get_piece(square)
                piece_ahead = self.get_piece(square_ahead)
                # if square == "b7" and direction_x == 0 and direction_y == 1:
                #     print("piece ahead " + piece_ahead)
                #     self.draw_simple()
                if piece_ahead is None:
                    squares_ahead.append(square_ahead)
                if squares_ahead_player is not None and (piece is None or squares_ahead_player != self.get_player_from_square(square)):
                    squares_ahead.append(square_ahead)
                break
            if limit is not None:
                break
        # if square == "b7" and direction_x == 0 and direction_y == 1:
        #     print("get_squares_ahead")
        #     print(squares_ahead)
        return squares_ahead

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
        attacking_player = self.get_player_from_square(square)
        if piece.lower() == "p":
            attack_directions = [(-1, direction), (1, direction)]
            attack_range = 1
        if piece.lower() == "k":
            attack_directions = [
                (1,  -1), (1,  0), (1,  1),
                (0,  -1),          (0,  1), 
                (-1, -1), (-1, 0), (-1, 1)
            ]
            attack_range = 1

        for i in range(attack_range):
            for attack_direction in attack_directions:
                attackable_square = (column + attack_direction[0] * (i + 1), row + attack_direction[1] * (i + 1))
                attackable_squares.append(attackable_square)
        for attackable_square in attackable_squares:
            target_square = self.get_file(attackable_square[0]) + self.get_row(attackable_square[1])
            piece = self.get_piece(target_square)
            if piece is not None:
                piece_player = self.get_player_from_square(target_square)
                other_player = self.get_other_player(attacking_player)
                if piece_player == other_player:
                    attacked_pieces.append(target_square)
        return attacked_pieces

    def get_player_from_square(self, square):
        piece = self.get_piece(square)
        if piece == None:
            raise Exception(f"square {square} is empty")
        return self.LIGHT_PLAYER if piece.isupper() else self.DARK_PLAYER
    
    def get_legal_moves(self, piece:str, square):
        legal_moves = []
        # self.draw_simple()
        # print("piece")
        # print(piece)
        piece = piece.upper()
        if piece == self.PAWN:
            legal_moves.extend(self.get_pawn_legal_moves(square))
        if piece == self.BISHOP:
            legal_moves.extend(self.get_bishop_legal_moves(square))
        if piece == self.KNIGHT:
            legal_moves.extend(self.get_knight_legal_moves(square))
        if piece == self.ROOK:
            legal_moves.extend(self.get_rook_legal_moves(square))
        if piece == self.QUEEN:
            legal_moves.extend(self.get_queen_legal_moves(square))
        if piece == self.KING:
            legal_moves.extend(self.get_king_legal_moves(square))
            legal_moves.extend(self.get_short_castle_move(square))
            legal_moves.extend(self.get_long_castle_move(square))
        return legal_moves

    def move(self, from_square, to_square):
        piece = self.get_piece(from_square)
        if piece == self.KING:
            if self.get_player_from_square(from_square) == self.LIGHT_PLAYER:
                self.has_white_king_moved = True
            else:
                self.has_black_king_moved = True
        if piece == self.ROOK:
            if self.get_player_from_square(from_square) == self.LIGHT_PLAYER:
                if from_square == "h1":
                    self.has_white_short_castle_rook_moved = True
                if from_square == "a1":
                    self.has_white_long_castle_rook_moved = True
            else:
                if from_square == "h8":
                    self.has_black_short_castle_rook_moved = True
                if from_square == "a8":
                    self.has_black_long_castle_rook_moved = True

        self.configuration[to_square] = self.configuration.get(from_square)
        self.configuration[from_square] = None

    def _is_attacking_piece(self, attacking_player, attacked_square):
        return attacking_player != self.get_player_from_square(attacked_square)

    def _get_attacking_player(self, king_square):
        return self.DARK_PLAYER if self.get_position_player(king_square) == self.LIGHT_PLAYER else self.LIGHT_PLAYER

    def is_in_check(self, king_square:str):
        attacking_player = self._get_attacking_player(king_square)
        attacking_squares = []
        for square in self.configuration.keys():
            if self.configuration.get(square) is not None:
                if self._is_attacking_piece(attacking_player, square):
                    attacking_squares.append(square)
        attacked_squares = []
        for attacking_square in attacking_squares:
            attacked_squares.extend(self.get_legal_moves(self.get_piece(attacking_square), attacking_square))
        return king_square in attacked_squares
    
    def is_checkmate(self, king_square:str):
        king = self.get_piece(king_square)
        return self.is_in_check(king_square) and len(self.get_legal_moves(king, king_square)) == 0
    
    def switch_player(self):
        self.current_player = self.LIGHT_PLAYER if self.current_player == self.DARK_PLAYER else self.DARK_PLAYER
    
    def is_stalemate(self, player):
        for square in self.configuration.keys():
            piece = self.configuration.get(square)
            if piece is not None and piece.lower() == "k":
                if player == self.LIGHT_PLAYER and piece.isupper():
                    king_square = square
                if player == self.DARK_PLAYER and piece.islower():
                    king_square = square
        king = self.get_piece(king_square)
        return not self.can_player_move_any_piece_except_king(player) and not self.is_in_check(king_square) and len(self.get_legal_moves(king, king_square)) == 0
    
    def get_player_pieces(self, player) -> dict:
        player_pieces = {}
        for square, piece in self.configuration.items():
            if piece is not None:
                if player == self.LIGHT_PLAYER and piece.isupper():
                    player_pieces[square] = piece
                if player == self.DARK_PLAYER and piece.islower():
                    player_pieces[square] = piece
        return player_pieces
    
    def can_player_move_any_piece_except_king(self, player):
        pieces = self.get_player_pieces(player)
        for piece, square in pieces.items():
            print("---------")
            print(piece, square)
            print(self.get_legal_moves(piece, square))
            if piece.lower() != "k" and len(self.get_legal_moves(piece, square)) > 0:
                return True
        return False
    
    def __str__(self) -> str:
        return self.configuration
    
    def draw_simple(self):
        for line in range(self.rows):
            if line == 0:
                print()
                for column in range(self.columns):
                    print(" _", end="")
                print()
            for column in range(self.columns):
                row = self.get_row(line)
                file = self.get_file(column)
                square = file + row
                if self.configuration.get(square) == None:
                    square_content = " "
                else:
                    square_content = self.configuration.get(square)
                print(f"|{square_content}", end="")
            print("|")
            for column in range(self.columns):
                print("|_", end="")
            print("|")