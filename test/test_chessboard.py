import chessboard
import unittest

class TestChessboard(unittest.TestCase):

    def test_get_file(self):
        chessBoard = chessboard.ChessBoard(100)
        assert "a" == chessBoard.get_file(0)
        assert "b" == chessBoard.get_file(1)
        assert "c" == chessBoard.get_file(2)
        assert "d" == chessBoard.get_file(3)
        assert "e" == chessBoard.get_file(4)
        assert "f" == chessBoard.get_file(5)
        assert "g" == chessBoard.get_file(6)
        assert "h" == chessBoard.get_file(7)

    def test_get_row(self):
        chessBoard = chessboard.ChessBoard(100)
        for i in range(8):
            assert 8 - i == int(chessBoard.get_row(i))

    # def test_get_clicked_square(self):
    #     chessBoard = chessboard.ChessBoard(100)
    #     assert "a8" == chessboard.get_clicked_square((0,0))
    
    if __name__ == "__main__":
        pass

