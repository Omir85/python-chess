# Project backlog — Rules implementation

This file lists chess rules and their implementation status in the codebase.
Prefix legend:
- `*` fully implemented
- `+` being implemented / partially implemented
- (no prefix) not implemented at all

Phase 1

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
- * Pawn promotion (when a pawn reaches the far rank, it must be promoted to Queen/Rook/Bishop/Knight)

Special rules

- * Castling (short and long) — king and rook movement rules implemented
- * Check detection
- * Checkmate detection
- * Stalemate detection
- * Pin detection (restriction of moves because of pins)

Draw rules

- * Threefold repetition
- * Fifty-move rule
- * Insufficient material

Notes / references

- All chess rules documented above have been implemented.
- Implementation evidence found in `chessboard.py` and unit tests in `test/test_chessboard.py`.

Phase 2

Now that the base game rules are implemented, we can add features to enhance the user experience and make the game more enjoyable.

- Players can resign
- Players can offer a draw
- When a player offers a draw, the opponent can accept or decline the offer
- If the draw offer is accepted, the game ends in a draw
- If the draw offer is declined, the player cannot ask again this turn, but can ask again in future turns
- If the draw offer is declined, the game continues as normal
- Display a window when the game ends for any reason (checkmate, stalemate, draw, resignation)
- Display a checkmate message when checkmate occurs
- Display a stalemate message when stalemate occurs
- Display a draw message when a draw occurs
- Display a resignation message when a player resigns
- Move history (displaying past moves)
- Undo functionality (allowing players to take back moves)
- Arrows (visual indicators for moves)
- Color checked king (highlighting the king in check)
- Color checkmated king (highlighting the king in checkmate)
- Area for taken pieces (displaying captured pieces)
- Save game (allowing players to save their current game state)
- Restore game (allowing players to load a saved game state)
- Archive game (allowing players to archive completed games)
- Replay archived game (allowing players to replay archived games)
- Play game from FEN

Phase 3

Now that we have a working game playable by humans, we can add an AI opponent to allow for single-player mode.

- Implement a basic AI opponent (e.g., random move selection)
- Allow players to choose to play against the AI
- Allow the AI player to resign or to offer a draw

Phase 4

We're getting in the interesting part, where the AI will play against itself and learn from it. This will involve implementing a more sophisticated AI algorithm (e.g., Minimax with alpha-beta pruning) and allowing the AI to play games against itself to improve its decision-making over time.

- Allow 2 AIs to play against each other (for testing and demonstration purposes)
- Make sure the AI never resigns when self-playing
- Implement a system where AI will learn from self-play (e.g., using reinforcement learning techniques)

