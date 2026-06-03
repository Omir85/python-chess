# Project backlog — Rules implementation

This file lists chess rules and their implementation status in the codebase.
Prefix legend:
- `*` fully implemented
- `+` being implemented / partially implemented
- (no prefix) not implemented at all

Overall rules

- * White moves first (turn order enforced)
- * Players alternate turns
- * A move is legal only if it does not leave/move the player's own king in check (move validation)
- * The king cannot be captured; game ends when checkmate occurs

Piece & move rules

- * Rook: any number of squares along rank or file
- * Bishop: any number of squares diagonally
- * Queen: any number of squares in any direction
- * Knight: L-shape (2x1 or 1x2) and can jump over pieces
- * King: one square in any direction (validated to avoid moving into check)
- * Kings cannot move to adjacent squares (kings cannot touch)
- * Pieces capture when moving (captures supported)

Pawn rules

- * Pawns move forward only
- * * Pawn double-step from starting rank is supported
- * Pawns capture one square diagonally forward
- * * En passant capture is implemented
-  Pawn promotion (when a pawn reaches the far rank, it must be promoted to Queen/Rook/Bishop/Knight)

Special rules

- * Castling (short and long) — king and rook movement rules implemented
- * Check detection
- * Checkmate detection
- * Stalemate detection
-  Pin detection (restriction of moves because of pins) — not implemented

Draw rules

-  Threefold repetition — not implemented
-  Fifty-move rule — not implemented
-  Insufficient material — not implemented

Notes / references

- Implementation evidence found in `chessboard.py` and unit tests in `test/test_chessboard.py`.
- Known bug: pawn promotion is not implemented (see `bugs.txt`).

