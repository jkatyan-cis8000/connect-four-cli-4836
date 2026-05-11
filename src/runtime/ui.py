from src.types import Player
from src.service.board import Board
from src.service.game import Game


def display_board(board: Board) -> None:
    print(str(board))
    print()


def get_player_input(player: Player) -> int:
    prompt = f"Player {player.value}, choose column (0-6): "
    while True:
        try:
            col = int(input(prompt))
            return col
        except ValueError:
            print("Please enter a number.")


def display_winner(player: Player) -> None:
    print(f"Player {player.value} wins!")


def display_draw() -> None:
    print("It's a draw!")


def display_invalid_move(message: str) -> None:
    print(message)


def run_game_loop(game: Game, ui_module) -> None:
    """Main game loop driven by UI layer."""
    while not game.is_game_over():
        current_player = game.get_current_player()
        col = ui_module.get_player_input(current_player)

        result = game.make_move(col)

        if not result.success:
            ui_module.display_invalid_move("Column is full. Try again.")
            continue

        ui_module.display_board(game.board)

        if result.game_over:
            if result.draw:
                ui_module.display_draw()
            else:
                ui_module.display_winner(result.winner)
