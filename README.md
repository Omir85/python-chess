# python-chess

Project created to train on python / pygame to develop a chess game.

PROJECT PHASES (* == Done):
* Phase 1: Board is displayed with rows and files
* Phase 2: Pieces are on the board
* Phase 2.5: Implement chess notation to quickload a board
* Phase 3: Pieces can move
* Phase 3.5: Castling (short and long)
* Phase 4: Pieces can take
* Phase 5: Check
Phase 5.1: Block
Phase 5.2: Pin
Phase 6: Stalemate
* Phase 7: Checkmate
Phase 8: Promotion
Phase 9: En passant
Phase 10: Implement time
Phase 11: Draw

RULES SECTION

Overall rules
- Pieces and pawns can move except if it puts moving player's king in check (Pin)
- Pieces take when moving
- Pawns can only take on the 2 forward diagonal squares
- The king is in check if it would be taken at the next turn
- The king is in checkmate when it is in check and it has no legal move
- Stalemate is declared when on player's turn, player has no legal move with any piece

Move rules:
- Rook can move any number of squares in linear direction (rows and files)
- Knight can move 2x1 or 1x2
- Knight can jump over pieces
- Bishop can move any number of squares in diagonal direction
- Queen can move any number of squares in any direction
- King can move 1 square in any direction as long as not in check after
- Pawns when on starting row can move 2 squares forward, otherwise can move only 1 square forward

Castling rules:
- Apply only for the king
- If no piece between the king and any of the rooks, the king can move 2 squares in the direction of the rook, and the rook will move towards the center next to the king
- King must not have already moved
- Castling rook must not have already moved
- Castling cannot be performed if any of the squares between the rook and the king are under attack (cannot castle through a check)

Draw rules:
- Repeat moves 3 times
- Only the kings remain on the board
-- Extension: Insufficient material
- No piece captured and no pawn advanced after 50 moves

Unspoken rule:
- Kings cannot touch