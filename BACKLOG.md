# Project Backlog — Implementation Status

This document tracks implementation status aligned with the README project phases.

Legend:
- `*` = Fully implemented
- `+` = Partially implemented / In progress
- (no prefix) = Not implemented

---

## Core Game Rules (Phases 1-11 from README)

### Phase 1: Board Display ✓
- * Board is displayed with rows (1-8) and files (a-h)
- * Square colors alternate correctly (dark/light)
- * Piece symbols are shown correctly

### Phase 2: Piece Placement ✓
- * All pieces are placed in standard starting positions
- * Piece display uses correct Unicode symbols

### Phase 2.5: Chess Notation ✓
- * FEN notation support (loading/saving positions)
- * Move notation in move history

### Phase 3: Basic Movement ✓
- * Rook moves: any number of squares horizontally/vertically
- * Bishop moves: any number of squares diagonally
- * Queen moves: any number of squares in any direction
- * Knight moves: L-shape (2x1 or 1x2), can jump over pieces
- * King moves: 1 square in any direction
- * Pawn moves: 1 square forward (or 2 from starting rank)
- * Move validation: pieces cannot move through other pieces
- * Turn order: White moves first, players alternate

### Phase 3.5: Castling ✓
- * Short castle: King moves 2 squares toward h-file rook
- * Long castle: King moves 2 squares toward a-file rook
- * Validation: king and rook must not have moved previously
- * Validation: no pieces between king and rook
- * Validation: king cannot castle through/into check
- * Rook moves correctly during castling

### Phase 4: Captures ✓
- * Piece captures opponent pieces by moving to their square
- * Pawn captures: 1 square diagonally forward only
- * En passant: special pawn capture when opponent double-steps
- * Captured pieces are removed from the board

### Phase 5: Check Detection ✓
- * Simple check condition: king is under attack

### Phase 5.1: Block (Restricting Moves Under Check) ✓
- * King must not move to an attacked square (implemented in Phase 5.2)
- * Pieces cannot move if it leaves king in check (pin restriction)

### Phase 5.2: Pin Detection ✓
- * Full pin detection implemented
- * Pinned pieces cannot move in ways that expose king to check
- * Pin filtering applies to all piece types
- * Non-recursive attack detection to avoid circular dependencies

### Phase 6: Stalemate ✓
- * Stalemate detection: player has no legal moves and is not in check
- * Game ends in draw when stalemate occurs

### Phase 7: Checkmate ✓
- * Checkmate detection: player is in check and has no legal moves
- * Game ends when checkmate occurs

### Phase 8: Pawn Promotion ✓
- * White pawns promote to Queen when reaching rank 8
- * Black pawns promote to Queen when reaching rank 1
- * Default promotion piece is Queen
- Note: Current implementation auto-promotes to Queen; choice UI not yet implemented

### Phase 9: En Passant ✓
- * En passant capture available when opponent pawn double-steps
- * Correct pawn removal during en passant capture
- * En passant only available immediately after opponent double-step

### Phase 10: Implement Time ⏳
- (Not yet implemented)
- Planned: Chess clock implementation with time controls

### Phase 11: Draw Conditions ✓
- * Threefold repetition: draw when same position repeats 3 times
- * Fifty-move rule: draw when 50 moves pass without pawn move or capture
- * Insufficient material: draw when only kings remain (or king + minor pieces)

---

## Enhanced Features (Planned Phases)

### Phase 12: Game UI Enhancements
- Move history display
- Undo functionality
- Visual arrows for suggested moves
- Highlight checked king
- Highlight checkmated king
- Captured pieces display area
- Game end window (checkmate/stalemate/draw/resignation)

### Phase 13: Game Persistence
- Save game to file
- Load saved game
- Archive completed games
- Replay archived games

### Phase 14: Player Features
- Player resignation
- Draw offers and negotiations
- Configurable starting positions (FEN)

### Phase 15: AI Opponent

#### Phase 15.1: Basic AI
- Random move selection AI
- Single-player vs AI mode
- AI can resign or offer draws

#### Phase 15.2: Advanced AI
- Minimax algorithm with alpha-beta pruning
- Self-play: 2 AIs can play against each other
- AI improvement through self-play
- Reinforcement learning integration

---

## Testing Status

- Total unit tests: 52
- Test coverage: All implemented rules have comprehensive unit tests
- All tests passing: ✓
- Bug verification tests: All documented bugs verified and fixed ✓

---

## Implementation Summary

**Core Game Status: COMPLETE ✓**
- All chess rules except Phase 10 (time) are fully implemented
- Phase 5.1 (Block) is fully covered by Phase 5.2 (Pin detection)
- Core game is fully playable and regulation-compliant

**Remaining Work:**
- Phase 10: Time/clock implementation
- Phase 12-15: UI enhancements, persistence, and AI features

