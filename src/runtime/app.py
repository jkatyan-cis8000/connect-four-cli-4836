from src.config import ROWS, COLS
from src.service.board import Board
from src.service.game import Game
from src.ui.terminal import GameUI


def create_game() -> tuple[Game, GameUI]:
    board = Board()
    game = Game(board)
    ui = GameUI()
    return game, ui


def main() -> None:
    """Entry point for runtime to initiate game setup."""
    pass


if __name__ == '__main__':
    main()
