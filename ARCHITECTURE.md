# ARCHITECTURE.md

Written by team-lead before spawning teammates. This is the shared blueprint —
teammates read it to understand what they are building and how their module fits.
Update it when the structure changes; do not let it drift from the actual code.

## Module Structure

- src/types.py: Type definitions for Player, CellState, Board, GameStatus, MoveResult
- src/config.py: Game constants (ROWS=6, COLS=7, WIN_LENGTH=4)
- src/service/board.py: Board class with move validation, win detection, grid management
- src/service/game.py: Game class with turn management, move execution, game state
- src/ui/terminal.py: Terminal rendering, user input parsing for column selection
- src/runtime/app.py: Main application entry point, orchestrates game loop
- src/utils/terminal.py: Helper functions for terminal output formatting

## Interfaces

### Board (service/board.py)
- `__init__(rows: int, cols: int)`: Initialize empty grid
- `drop_piece(col: int, player: Player) -> tuple[int, bool]`: Drop piece, return (row, success)
- `is_valid_move(col: int) -> bool`: Check if column is valid
- `is_full() -> bool`: Check if board is full
- `check_winner() -> Player | None`: Check for winner (horizontal, vertical, diagonal)
- `get_cell(row: int, col: int) -> CellState`: Get cell state
- `__str__() -> str`: String representation for display

### Game (service/game.py)
- `__init__(board: Board)`: Initialize game with board
- `make_move(col: int) -> MoveResult`: Execute move and return result
- `get_current_player() -> Player`: Get current player
- `is_game_over() -> bool`: Check if game ended
- `get_winner() -> Player | None`: Get winning player
- `is_draw() -> bool`: Check if draw
- `reset() -> None`: Reset game state

### UI (ui/terminal.py)
- `display_board(board: Board) -> None`: Render current board state
- `get_player_input(player: Player) -> int`: Get column choice from player
- `display_winner(player: Player) -> None`: Announce winner
- `display_draw() -> None`: Announce draw
- `display_invalid_move(message: str) -> None`: Show error for invalid move

### Runtime (runtime/app.py)
- `main() -> None`: Entry point, manages game loop
- `create_game() -> Game`: Factory to create game instance

## Shared Data Structures

```python
# Player enum: PLAYER_1 = 'X', PLAYER_2 = 'O'
class Player(Enum):
    PLAYER_1 = 'X'
    PLAYER_2 = 'O'

# CellState enum: EMPTY = '_', PLAYER_1, PLAYER_2
class CellState(Enum):
    EMPTY = '_'
    PLAYER_1 = 'X'
    PLAYER_2 = 'O'

# MoveResult dataclass
class MoveResult:
    success: bool
    row: int
    player: Player
    game_over: bool
    winner: Player | None
    draw: bool

# GameStatus enum
class GameStatus(Enum):
    ONGOING = 'ongoing'
    PLAYER_1_WON = 'player1_won'
    PLAYER_2_WON = 'player2_won'
    DRAW = 'draw'
```

## External Dependencies

No external dependencies required. Pure Python implementation using standard library.
