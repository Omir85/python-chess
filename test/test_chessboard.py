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
        assert f"{self.board}" == "Dark:(a8:R)(b8:N)(c8:B)(d8:Q)(e8:K)(f8:B)(g8:N)(h8:R)(a7:p)(b7:p)(c7:p)(d7:p)(e7:p)(f7:p)(g7:p)(h7:p)\nLight:(a2:p)(b2:p)(c2:p)(d2:p)(e2:p)(f2:p)(g2:p)(h2:p)(a1:R)(b1:N)(c1:B)(d1:Q)(e1:K)(f1:B)(g1:N)(h1:R)"
    
    def test_get_square_coordinates(self):
        square = "a8"
        coordinates = self.board.get_square_coordinates(square)
        assert (0, -20) == coordinates
        square = "h1"
        coordinates = self.board.get_square_coordinates(square)
        assert (700, 680) == coordinates

    def test_did_click_on_player_piece(self):
        square = "a1"
        current_player = colors.WHITE_COLOR
        assert True == self.board.did_click_on_player_piece(current_player, square)
        current_player = colors.BLACK_COLOR
        assert False == self.board.did_click_on_player_piece(current_player, square)
        square = "h8"
        current_player = colors.WHITE_COLOR
        assert False == self.board.did_click_on_player_piece(current_player, square)
        current_player = colors.BLACK_COLOR
        assert True == self.board.did_click_on_player_piece(current_player, square)
        square = "e4"
        current_player = colors.WHITE_COLOR
        assert False == self.board.did_click_on_player_piece(current_player, square)
        current_player = colors.BLACK_COLOR
        assert False == self.board.did_click_on_player_piece(current_player, square)
        
    def test_get_clicked_player_piece(self):
        assert self.board.ROOK == self.board.get_clicked_player_piece("a1")
        assert self.board.KNIGHT == self.board.get_clicked_player_piece("b1")
        assert self.board.BISHOP == self.board.get_clicked_player_piece("c1")
        assert self.board.QUEEN == self.board.get_clicked_player_piece("d1")
        assert self.board.KING == self.board.get_clicked_player_piece("e1")
        assert self.board.BISHOP == self.board.get_clicked_player_piece("f1")
        assert self.board.KNIGHT == self.board.get_clicked_player_piece("g1")
        assert self.board.ROOK == self.board.get_clicked_player_piece("h1")
        assert self.board.PAWN == self.board.get_clicked_player_piece("a2")
        assert self.board.PAWN == self.board.get_clicked_player_piece("b2")
        assert self.board.PAWN == self.board.get_clicked_player_piece("c2")
        assert self.board.PAWN == self.board.get_clicked_player_piece("d2")
        assert self.board.PAWN == self.board.get_clicked_player_piece("e2")
        assert self.board.PAWN == self.board.get_clicked_player_piece("f2")
        assert self.board.PAWN == self.board.get_clicked_player_piece("g2")
        assert self.board.PAWN == self.board.get_clicked_player_piece("h2")
        try:
            self.board.get_clicked_player_piece("a3")
        except Exception as e:
            assert "No piece found on a3" == f"{e}"

    def test_get_legal_moves(self):
        legal_moves = self.board.get_legal_moves("p", "a2")
        assert len(legal_moves) == 2
        assert "a3" in legal_moves
        assert "a4" in legal_moves
        legal_moves = self.board.get_legal_moves("p", "b2")
        assert len(legal_moves) == 2
        assert "b3" in legal_moves
        assert "b4" in legal_moves
        # self.board.configuration.get(self.board.DARK_PLAYER)["a3"] = "p"
        # legal_moves = self.board.get_legal_moves("p", "a3")
        # print(legal_moves)
        # assert len(legal_moves) == 0

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

    if __name__ == "__main__":
        pass

