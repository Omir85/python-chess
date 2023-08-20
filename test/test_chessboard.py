import chessboard
import unittest

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

    if __name__ == "__main__":
        pass

