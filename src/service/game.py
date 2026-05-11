from src.types import Player, CellState, MoveResult, GameStatus
from src.service.board import Board


class Game:
    def __init__(self, board: Board) -> None:
        self.board = board
        self.current_player = Player.PLAYER_1
        self.game_status = GameStatus.ONGOING

    def make_move(self, col: int) -> MoveResult:
        if self.game_status != GameStatus.ONGOING:
            return MoveResult(
                success=False,
                row=-1,
                player=self.current_player,
                game_over=True,
                winner=None,
                draw=True,
            )

        row, success = self.board.drop_piece(col, self.current_player)
        if not success:
            return MoveResult(
                success=False,
                row=row,
                player=self.current_player,
                game_over=False,
                winner=None,
                draw=False,
            )

        winner = self.board.check_winner()
        if winner is not None:
            self.game_status = (
                GameStatus.PLAYER_1_WON
                if winner == Player.PLAYER_1
                else GameStatus.PLAYER_2_WON
            )
            return MoveResult(
                success=True,
                row=row,
                player=self.current_player,
                game_over=True,
                winner=winner,
                draw=False,
            )

        if self.board.is_full():
            self.game_status = GameStatus.DRAW
            return MoveResult(
                success=True,
                row=row,
                player=self.current_player,
                game_over=True,
                winner=None,
                draw=True,
            )

        self._switch_player()
        return MoveResult(
            success=True,
            row=row,
            player=self.current_player,
            game_over=False,
            winner=None,
            draw=False,
        )

    def _switch_player(self) -> None:
        self.current_player = (
            Player.PLAYER_2
            if self.current_player == Player.PLAYER_1
            else Player.PLAYER_1
        )

    def get_current_player(self) -> Player:
        return self.current_player

    def is_game_over(self) -> bool:
        return self.game_status != GameStatus.ONGOING

    def get_winner(self) -> Player | None:
        if self.game_status == GameStatus.PLAYER_1_WON:
            return Player.PLAYER_1
        if self.game_status == GameStatus.PLAYER_2_WON:
            return Player.PLAYER_2
        return None

    def is_draw(self) -> bool:
        return self.game_status == GameStatus.DRAW

    def reset(self) -> None:
        self.board = Board()
        self.current_player = Player.PLAYER_1
        self.game_status = GameStatus.ONGOING

    def make_move(self, col: int) -> MoveResult:
        if self.game_status != GameStatus.ONGOING:
            return MoveResult(
                success=False,
                row=-1,
                player=self.current_player,
                game_over=True,
                winner=None,
                draw=self.game_status == GameStatus.DRAW,
            )

        row, success = self.board.drop_piece(col, self.current_player)
        if not success:
            return MoveResult(
                success=False,
                row=row,
                player=self.current_player,
                game_over=False,
                winner=None,
                draw=False,
            )

        if self.board.check_winner(row, col, self.current_player):
            self.game_status = (
                GameStatus.PLAYER_1_WON
                if self.current_player == Player.PLAYER_1
                else GameStatus.PLAYER_2_WON
            )
            return MoveResult(
                success=True,
                row=row,
                player=self.current_player,
                game_over=True,
                winner=self.current_player,
                draw=False,
            )

        if self.board.is_full():
            self.game_status = GameStatus.DRAW
            return MoveResult(
                success=True,
                row=row,
                player=self.current_player,
                game_over=True,
                winner=None,
                draw=True,
            )

        self._switch_player()
        return MoveResult(
            success=True,
            row=row,
            player=self.current_player,
            game_over=False,
            winner=None,
            draw=False,
        )

    def _switch_player(self) -> None:
        self.current_player = (
            Player.PLAYER_2
            if self.current_player == Player.PLAYER_1
            else Player.PLAYER_1
        )

    def get_current_player(self) -> Player:
        return self.current_player

    def is_game_over(self) -> bool:
        return self.game_status != GameStatus.ONGOING

    def get_winner(self) -> Player | None:
        if self.game_status == GameStatus.PLAYER_1_WON:
            return Player.PLAYER_1
        if self.game_status == GameStatus.PLAYER_2_WON:
            return Player.PLAYER_2
        return None

    def is_draw(self) -> bool:
        return self.game_status == GameStatus.DRAW

    def reset(self) -> None:
        self.board = Board()
        self.current_player = Player.PLAYER_1
        self.game_status = GameStatus.ONGOING
