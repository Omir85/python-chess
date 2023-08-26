import chessboard
import unittest
import colors

class TestChessboard(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        self.board = chessboard.ChessBoard(100)
        super().__init__(methodName)

    def test_get_file(self):
        assert "a" == self.board.get_file(0)
        assert "b" == self.board.get_file(1)
        assert "c" == self.board.get_file(2)
        assert "d" == self.board.get_file(3)
        assert "e" == self.board.get_file(4)
        assert "f" == self.board.get_file(5)
        assert "g" == self.board.get_file(6)
        assert "h" == self.board.get_file(7)

    def test_get_row(self):
        for i in range(8):
            assert 8 - i == int(self.board.get_row(i))

    def test_get_clicked_square(self):
        assert "a8" == self.board.get_clicked_square((0,0))
        assert "b8" == self.board.get_clicked_square((100,0))
        assert "c8" == self.board.get_clicked_square((200,0))
        assert "d8" == self.board.get_clicked_square((300,0))
        assert "e8" == self.board.get_clicked_square((400,0))
        assert "f8" == self.board.get_clicked_square((500,0))
        assert "g8" == self.board.get_clicked_square((600,0))
        assert "h8" == self.board.get_clicked_square((700,0))
    
    def test_str(self):
        assert f"{self.board.configuration}" == "{'a8': 'r', 'b8': 'n', 'c8': 'b', 'd8': 'q', 'e8': 'k', 'f8': 'b', 'g8': 'n', 'h8': 'r', 'a7': 'p', 'b7': 'p', 'c7': 'p', 'd7': 'p', 'e7': 'p', 'f7': 'p', 'g7': 'p', 'h7': 'p', 'a2': 'P', 'b2': 'P', 'c2': 'P', 'd2': 'P', 'e2': 'P', 'f2': 'P', 'g2': 'P', 'h2': 'P', 'a1': 'R', 'b1': 'N', 'c1': 'B', 'd1': 'Q', 'e1': 'K', 'f1': 'B', 'g1': 'N', 'h1': 'R'}"
    
    def test_get_square_coordinates(self):
        square = "a8"
        coordinates = self.board.get_square_coordinates(square)
        assert (0, -20) == coordinates
        square = "h1"
        coordinates = self.board.get_square_coordinates(square)
        assert (700, 680) == coordinates

    def test_did_click_on_player_piece(self):
        square = "a1"
        assert True == self.board.did_click_on_player_piece(square)
        self.board.switch_player()
        assert False == self.board.did_click_on_player_piece(square)
        square = "h8"
        self.board.switch_player()
        assert False == self.board.did_click_on_player_piece(square)
        self.board.switch_player()
        assert True == self.board.did_click_on_player_piece(square)
        square = "e4"
        self.board.switch_player()
        assert False == self.board.did_click_on_player_piece(square)
        self.board.switch_player()
        assert False == self.board.did_click_on_player_piece(square)
        
    def test_get_piece(self):
        assert self.board.ROOK == self.board.get_piece("a1")
        assert self.board.KNIGHT == self.board.get_piece("b1")
        assert self.board.BISHOP == self.board.get_piece("c1")
        assert self.board.QUEEN == self.board.get_piece("d1")
        assert self.board.KING == self.board.get_piece("e1")
        assert self.board.BISHOP == self.board.get_piece("f1")
        assert self.board.KNIGHT == self.board.get_piece("g1")
        assert self.board.ROOK == self.board.get_piece("h1")
        assert self.board.PAWN == self.board.get_piece("a2")
        assert self.board.PAWN == self.board.get_piece("b2")
        assert self.board.PAWN == self.board.get_piece("c2")
        assert self.board.PAWN == self.board.get_piece("d2")
        assert self.board.PAWN == self.board.get_piece("e2")
        assert self.board.PAWN == self.board.get_piece("f2")
        assert self.board.PAWN == self.board.get_piece("g2")
        assert self.board.PAWN == self.board.get_piece("h2")
        try:
            self.board.get_piece("a3")
        except Exception as e:
            assert "No piece found on a3" == f"{e}"

    def test_get_white_pawn_legal_moves(self):
        legal_moves = self.board.get_pawn_legal_moves("a2")
        assert len(legal_moves) == 2
        assert "a3" in legal_moves
        assert "a4" in legal_moves
        legal_moves = self.board.get_pawn_legal_moves("b2")
        assert len(legal_moves) == 2
        assert "b3" in legal_moves
        assert "b4" in legal_moves
        # Put a pawn in a non-starting position
        self.board.configuration["h3"] = "P"
        legal_moves = self.board.get_pawn_legal_moves("h3")
        assert len(legal_moves) == 1
        assert "h4" in legal_moves
        # Block 2 squares in front of a pawn
        self.board.configuration["a4"] = "p"
        legal_moves = self.board.get_pawn_legal_moves("a2")
        assert len(legal_moves) == 1
        assert "a3" in legal_moves
        # Add a piece to take for the pawn
        self.board.configuration["b3"] = "b"
        legal_moves = self.board.get_pawn_legal_moves("a2")
        assert len(legal_moves) == 2
        assert "b3" in legal_moves
        assert "a3" in legal_moves
        # Block the square in front of the pawn
        self.board.configuration["a3"] = "p"
        legal_moves = self.board.get_pawn_legal_moves("a2")
        assert len(legal_moves) == 1
        assert "b3" in legal_moves
        # Remove the piece to take for the pawn
        self.board.configuration["b3"] = None
        legal_moves = self.board.get_pawn_legal_moves("a2")
        assert len(legal_moves) == 0
        # Leave only the piece in front of the pawn
        self.board.configuration["a4"] = None
        legal_moves = self.board.get_pawn_legal_moves("a2")
        assert len(legal_moves) == 0
        # Reinitialize the board in a specific configuration
        self.board = chessboard.ChessBoard(100, fen="K7/1rq3P1/8/8/8/8/8/8 w KQkq - 0 1")
        legal_moves = self.board.get_pawn_legal_moves("g7")
        assert len(legal_moves) == 1
        self.board = chessboard.ChessBoard(100, "K7/1r6/2q5/8/8/8/P7/8" + self.board.get_default_fen_end())
        legal_moves = self.board.get_pawn_legal_moves("a2")
        assert len(legal_moves) == 2

    def test_is_pawn_stuck(self):
        assert False == self.board.is_pawn_stuck("a2")
        self.board.configuration["a3"] = "p"
        assert True == self.board.is_pawn_stuck("a2")

    def test_get_black_pawn_legal_moves(self):
        legal_moves = self.board.get_pawn_legal_moves("a7")
        assert len(legal_moves) == 2
        assert "a6" in legal_moves
        assert "a5" in legal_moves
        legal_moves = self.board.get_pawn_legal_moves("e7")
        assert len(legal_moves) == 2
        assert "e6" in legal_moves
        assert "e5" in legal_moves

    def test_get_pieces_attacked_by(self):
        self.board.move("b7", "b3")
        attacked_squares = self.board.get_pieces_attacked_by("a2")
        assert len(attacked_squares) == 1
        assert "b3" in attacked_squares

        attacked_squares = self.board.get_pieces_attacked_by("h2")
        assert len(attacked_squares) == 0
        self.board.move("g2", "g3")
        attacked_squares = self.board.get_pieces_attacked_by("h2")
        assert len(attacked_squares) == 0
        
        self.board.move("g7", "g3")
        attacked_squares = self.board.get_pieces_attacked_by("h2")
        assert len(attacked_squares) == 1
        attacked_squares = self.board.get_pieces_attacked_by("g3")
        assert len(attacked_squares) == 2

    def test_get_player_from_square(self):
        try:
            self.board.get_player_from_square("a3")
        except Exception as e:
            assert "square a3 is empty" == f"{e}"
        try:
            self.board.get_player_from_square("a4")
        except Exception as e:
            assert "square a4 is empty" == f"{e}"
        assert self.board.LIGHT_PLAYER == self.board.get_player_from_square("a1")
        assert self.board.DARK_PLAYER == self.board.get_player_from_square("a8")

    def test_move(self):
        from_square = "a2"
        to_square = "a4"
        assert "P" == self.board.get_piece(from_square)
        assert None == self.board.get_piece(to_square)
        self.board.move(from_square, to_square)
        assert None == self.board.get_piece(from_square)
        assert "P" == self.board.get_piece(to_square)

    def test_get_bishop_legal_moves(self):
        legal_moves = self.board.get_bishop_legal_moves("c1")
        assert len(legal_moves) == 0
        self.board.move("b2", "b3")
        legal_moves = self.board.get_bishop_legal_moves("c1")
        assert len(legal_moves) == 2
        self.board.move("d2", "d3")
        legal_moves = self.board.get_bishop_legal_moves("c1")
        assert len(legal_moves) == 7
        self.board.move("b3", "b2")
        legal_moves = self.board.get_bishop_legal_moves("c1")
        assert len(legal_moves) == 5
        self.board.move("c1", "b2")
        legal_moves = self.board.get_bishop_legal_moves("b2")
        assert len(legal_moves) == 7
        self.board.move("f7", "f6")
        legal_moves = self.board.get_bishop_legal_moves("b2")
        assert len(legal_moves) == 6
        self.board.move("e7", "e5")
        legal_moves = self.board.get_bishop_legal_moves("b2")
        assert len(legal_moves) == 5
        self.board.move("e5", "e4")
        legal_moves = self.board.get_bishop_legal_moves("b2")
        assert len(legal_moves) == 6

    def test_out_of_bounds(self):
        assert False == self.board.is_on_board("d0")

    def test_get_squares_ahead(self):
        # Initial Queen's bishop position
        squares_ahead = self.board.get_squares_ahead("c1", -1, 1)
        assert len(squares_ahead) == 0
        squares_ahead = self.board.get_squares_ahead("c1", 1, 1)
        assert len(squares_ahead) == 0
        squares_ahead = self.board.get_squares_ahead("c1", 1, -1)
        assert len(squares_ahead) == 0
        squares_ahead = self.board.get_squares_ahead("c1", -1, -1)
        assert len(squares_ahead) == 0
        # Only white player moves here
        # b3 then bishop b2
        self.board.move("b2", "b3")
        self.board.move("c1", "b2")
        squares_ahead = self.board.get_squares_ahead("b2", -1, 1)
        assert len(squares_ahead) == 1
        squares_ahead = self.board.get_squares_ahead("b2", 1, 1)
        assert len(squares_ahead) == 5
        squares_ahead = self.board.get_squares_ahead("b2", 1, -1)
        assert len(squares_ahead) == 1
        squares_ahead = self.board.get_squares_ahead("b2", -1, -1)
        assert len(squares_ahead) == 0
        # c3
        self.board.move("c2", "c3")
        squares_ahead = self.board.get_squares_ahead("b2", -1, 1)
        assert len(squares_ahead) == 1
        squares_ahead = self.board.get_squares_ahead("b2", 1, 1)
        assert len(squares_ahead) == 0
        squares_ahead = self.board.get_squares_ahead("b2", 1, -1)
        assert len(squares_ahead) == 1
        squares_ahead = self.board.get_squares_ahead("b2", -1, -1)
        assert len(squares_ahead) == 0

    def test_get_knight_moves(self):
        moves = self.board.get_knight_moves("b1", 1, 2)
        assert len(moves) == 2
        moves = self.board.get_knight_moves("b1", 2, 1)
        assert len(moves) == 1

    def test_get_knight_legal_moves(self):
        legal_moves = self.board.get_knight_legal_moves("b1")
        assert len(legal_moves) == 2
        self.board.move("b1", "c3")
        legal_moves = self.board.get_knight_legal_moves("c3")
        assert len(legal_moves) == 5
        self.board.move("c3", "d5")
        legal_moves = self.board.get_knight_legal_moves("d5")
        assert len(legal_moves) == 8
        # reset knight position
        self.board.move("d5", "b1")
        # c3 then a3 to block the knight's path
        self.board.move("c2", "c3")
        legal_moves = self.board.get_knight_legal_moves("b1")
        assert len(legal_moves) == 1
        self.board.move("a2", "a3")
        legal_moves = self.board.get_knight_legal_moves("b1")
        assert len(legal_moves) == 0
        # board edge test
        self.board.move("b2", "b6")
        legal_moves = self.board.get_knight_legal_moves("b6")
        assert len(legal_moves) == 6
    
    def test_get_rook_legal_moves(self):
        legal_moves = self.board.get_rook_legal_moves("a1")
        assert len(legal_moves) == 0
        self.board.move("a2", "a3")
        legal_moves = self.board.get_rook_legal_moves("a1")
        assert len(legal_moves) == 1
        self.board.move("a3", "a4")
        legal_moves = self.board.get_rook_legal_moves("a1")
        assert len(legal_moves) == 2
        self.board.move("a1", "a3")
        legal_moves = self.board.get_rook_legal_moves("a3")
        assert len(legal_moves) == 9
        self.board.move("a3", "b3")
        legal_moves = self.board.get_rook_legal_moves("b3")
        assert len(legal_moves) == 11
        self.board = chessboard.ChessBoard("8/1r6/8/8/8/8/8/8")
        legal_moves = self.board.get_rook_legal_moves("b7")
        # print("rook b7 legal moves")
        # print(legal_moves)
        # assert "b8" in legal_moves

    def test_get_queen_legal_moves(self):
        legal_moves = self.board.get_queen_legal_moves("d1")
        assert len(legal_moves) == 0
        self.board.move("d1", "d3")
        legal_moves = self.board.get_queen_legal_moves("d3")
        assert len(legal_moves) == 18
        self.board.move("d3", "d2")
        legal_moves = self.board.get_queen_legal_moves("d2")
        assert len(legal_moves) == 13

    def test_get_king_legal_moves(self):
        legal_moves = self.board.get_king_legal_moves("e1")
        assert len(legal_moves) == 0
        self.board.move("e2", "e4")
        legal_moves = self.board.get_king_legal_moves("e1")
        assert len(legal_moves) == 1
        self.board.move("e1", "e2")
        legal_moves = self.board.get_king_legal_moves("e2")
        assert len(legal_moves) == 4
        # Reset the board
        self.board = chessboard.ChessBoard(100)
        self.board.move("f2", "f3")
        legal_moves = self.board.get_king_legal_moves("e1")
        assert len(legal_moves) == 1
        # Put dark bishop on a checking square
        self.board.move("f8", "h4")
        legal_moves = self.board.get_king_legal_moves("e1")
        assert len(legal_moves) == 0
        # Reinitialize the board with new config
        fen = "8/8/8/8/8/8/8/8" + self.board.get_default_fen_end()
        self.board = chessboard.ChessBoard(100, fen)
        self.board.configuration["c2"] = "K"
        self.board.configuration["c3"] = "q"
        legal_moves = self.board.get_king_legal_moves("c2")
        assert self.board.configuration["c3"] == "q"

    def test_is_in_check(self):
        assert False == self.board.is_in_check("e1")
        self.board.move("d2", "d3")
        self.board.move("f2", "f3")
        self.board.move("f8", "b4")
        assert True == self.board.is_in_check("e1")
        self.board.move("e1", "f2")
        assert False == self.board.is_in_check("f2")

    def test_is_checkmate(self):
        self.board = chessboard.ChessBoard(100)
        assert False == self.board.is_checkmate("e1")
        self.board.move("d2", "d3")
        self.board.move("f8", "b4")
        assert True == self.board.is_checkmate("e1")
        self.board.move("f2", "f3")
        assert False == self.board.is_checkmate("e1")

    def test_get_short_castle_move(self):
        self.board.configuration["f1"] = None
        self.board.configuration["g1"] = None
        legal_moves = self.board.get_short_castle_move("e1")
        assert len(legal_moves) == 1
        assert "g1" in legal_moves
        # Queen b6
        self.board.move("d8", "b6")
        legal_moves = self.board.get_short_castle_move("e1")
        assert len(legal_moves) == 1
        assert "g1" in legal_moves
        # f3
        self.board.move("f2", "f3")
        legal_moves = self.board.get_short_castle_move("e1")
        # Not possible to castle through a check
        assert len(legal_moves) == 0
        self.board.move("e2", "e3")
        legal_moves = self.board.get_short_castle_move("e1")
        assert len(legal_moves) == 1
        assert "g1" in legal_moves
        self.board.move("h1", "g1")
        legal_moves = self.board.get_short_castle_move("e1")
        assert len(legal_moves) == 0
        self.board.move("g1", "h1")
        legal_moves = self.board.get_short_castle_move("e1")
        assert len(legal_moves) == 0
        assert "g1" not in legal_moves
    
    def test_long_castle(self):
        self.board.configuration["b1"] = None
        self.board.configuration["c1"] = None
        self.board.configuration["d1"] = None
        legal_moves = self.board.get_long_castle_move("e1")
        assert len(legal_moves) == 1
        assert "c1" in legal_moves
    
    def test_switch_player(self):
        assert self.board.LIGHT_PLAYER == self.board.current_player
        self.board.switch_player()
        assert self.board.DARK_PLAYER == self.board.current_player
        self.board.switch_player()
        assert self.board.LIGHT_PLAYER == self.board.current_player

    def test_is_stalemate(self):
        # Stalemate: White King in a8 and black Queen in c6
        self.board = chessboard.ChessBoard(100, "K7/1r6/2q5/8/8/8/8/8" + self.board.get_default_fen_end())
        assert self.board.is_stalemated(self.board.LIGHT_PLAYER)
        # Not stalemate: Same config but a white pawn is in a2
        self.board = chessboard.ChessBoard(100, "K7/1r6/2q5/8/8/8/P7/8" + self.board.get_default_fen_end())
        assert not self.board.is_stalemated(self.board.LIGHT_PLAYER)

    if __name__ == "__main__":
        pass

