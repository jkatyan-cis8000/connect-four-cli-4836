"""Game type definitions."""

from dataclasses import dataclass
from enum import Enum


class Player(Enum):
    PLAYER_1 = 'X'
    PLAYER_2 = 'O'


class CellState(Enum):
    EMPTY = '_'
    PLAYER_1 = 'X'
    PLAYER_2 = 'O'


class GameStatus(Enum):
    ONGOING = 'ongoing'
    PLAYER_1_WON = 'player1_won'
    PLAYER_2_WON = 'player2_won'
    DRAW = 'draw'


@dataclass
class MoveResult:
    success: bool
    row: int
    player: Player
    game_over: bool
    winner: Player | None
    draw: bool
