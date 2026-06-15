# python-chess

Project created to train on python / pygame to develop a chess game.

LICENSE
GNU Affero General Public License v3.0
See license.md for the license terms

SETUP VIRTUAL ENVIRONMENT

python -m venv venv

INSTALL THE REQUIREMENTS
pip install -r requirements.txt

LAUNCH INSTRUCTIONS

Run the virtual environment:
source venv/Script/activate

Run the game:
python main.py

Run the tests:
python -m unittest test/test_chessboard.py

GENERATE EXECUTABLE

python -m pip install PyInstaller
python -m PyInstaller --onefile --noconsole main.py

PROJECT PHASES & FEATURE BACKLOG

See `BACKLOG.md` for the full project phases, implementation status, and planned features. This repository's detailed backlog (done, in-progress, and planned items) is maintained in that file to avoid duplication.

RULES OF CHESS

This section summarizes the official rules of chess as implemented or intended for this project. It is written to be complete and unambiguous for game logic purposes.

1) Game basics
- Two players: White and Black. White moves first, then players alternate turns.
- Objective: checkmate the opponent's king (put the king under attack with no legal move to escape). A draw result is possible by the rules below.

2) Legal and illegal moves
- A move is legal only if it conforms to the movement rules of the piece and does not leave or place the player's own king in check.
- Players may not make a move that results in their own king being in check. Illegal moves are not allowed.

3) Piece movement and capture
- King: moves one square in any direction. The king cannot move into check.
- Queen: moves any number of squares along rank, file, or diagonal, until blocked by another piece. Captures by landing on an occupied enemy square.
- Rook: moves any number of squares along rank or file. Captures like the queen.
- Bishop: moves any number of squares diagonally.
- Knight: moves in an 'L' shape (two squares in one direction and then one perpendicular). Knights may jump over pieces.
- Pawn: moves forward one square. On its first move a pawn may move two squares forward if both squares are unoccupied. Pawns capture one square diagonally forward. Pawns cannot move or capture backward.

4) Special pawn rules
- En passant: If a pawn moves two squares from its starting rank and lands adjacent to an opponent pawn, that opponent pawn may capture it en passant on its immediately following move as if the pawn had moved only one square. The capturing pawn moves to the square the pawn passed over and the moved pawn is removed.
- Promotion: When a pawn reaches the opponent's back rank (rank 8 for White, rank 1 for Black) it is promoted immediately to a queen, rook, bishop, or knight of the same color. In this project default promotion is to a queen; a promotion choice UI may be added later.

5) Castling
- Castling is a joint king+rook move performed as follows: the king moves two squares toward a rook on the player's first rank, and that rook moves to the square the king passed over (ending adjacent to the king).
- Conditions for castling to be legal:
  - Neither the king nor the rook involved have previously moved.
  - There are no pieces between the king and the rook.
  - The king is not currently in check.
  - The squares that the king passes over, and the destination square, are not under attack by any enemy piece (the king may not castle through or into check).

6) Check, checkmate, and stalemate
- Check: a king is in check if it is under attack by one or more enemy pieces. Players must respond to check by making a move that removes the check on their turn.
- Checkmate: the king is in check and the side to move has no legal move to remove the check. The game ends with a win for the attacker.
- Stalemate: the side to move is not in check but has no legal move. The game is a draw.

7) Draw conditions
- Threefold repetition: If the same board position occurs three times with the same player to move and same rights (castling, en passant), a player may claim a draw.
- Fifty-move rule: If fifty consecutive full moves (i.e., 50 moves by each side, or 100 plies) occur without any pawn move or capture, a player may claim a draw. (Some sources use 50 half-moves; implement according to chosen convention — backlog notes track this.)
- Insufficient material: The game is a draw if checkmate is impossible with the material on the board (e.g., king vs. king, king and bishop vs. king, king and knight vs. king; specific exceptions apply for some combinations).
- Agreement: players may agree to a draw at any time.
