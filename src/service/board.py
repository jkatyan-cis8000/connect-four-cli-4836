"""Board class for grid management, move validation, and win detection."""

from src.config import COLS, ROWS, WIN_LENGTH
from src.types import CellState, Player


class Board:
    def __init__(self) -> None:
        self._grid: list[list[CellState]] = [
            [CellState.EMPTY for _ in range(COLS)] for _ in range(ROWS)
        ]

    def drop_piece(self, col: int, player: Player) -> tuple[int, bool]:
        if not self.is_valid_move(col):
            return -1, False
        for row in range(ROWS - 1, -1, -1):
            if self._grid[row][col] == CellState.EMPTY:
                self._grid[row][col] = CellState(player.value)
                return row, True
        return -1, False

    def is_valid_move(self, col: int) -> bool:
        if col < 0 or col >= COLS:
            return False
        return self._grid[0][col] == CellState.EMPTY

    def is_full(self) -> bool:
        return all(self._grid[0][col] != CellState.EMPTY for col in range(COLS))

    def check_winner(self) -> Player | None:
        for row in range(ROWS):
            for col in range(COLS):
                winner = self._check_direction(row, col)
                if winner:
                    return Player(winner)
        return None

    def _check_direction(self, row: int, col: int) -> Player | None:
        player = self._grid[row][col]
        if player == CellState.EMPTY:
            return None
        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1),
        ]
        for dr, dc in directions:
            if self._check_line(row, col, dr, dc, player):
                return Player(player.value)
        return None

    def _check_line(self, row: int, col: int, dr: int, dc: int, player: CellState) -> bool:
        for i in range(WIN_LENGTH):
            r, c = row + dr * i, col + dc * i
            if r < 0 or r >= ROWS or c < 0 or c >= COLS:
                return False
            if self._grid[r][c] != player:
                return False
        return True

    def get_cell(self, row: int, col: int) -> CellState:
        return self._grid[row][col]

    def __str__(self) -> str:
        lines = []
        for row in self._grid:
            lines.append(' '.join(cell.value for cell in row))
        return '\n'.join(lines)
