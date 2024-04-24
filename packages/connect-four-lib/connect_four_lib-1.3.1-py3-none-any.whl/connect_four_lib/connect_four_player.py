from duo_game_lib.player import Player

from connect_four_lib.connect_four_engine import ConnectFourEngine


class ConnectFourPlayer(Player):
    def __init__(self, elo) -> None:
        super().__init__()

        self.engine: ConnectFourEngine = ConnectFourEngine()
        self.elo: int = elo

    def play(self, move: str) -> str:
        if move:
            self.engine.add_move(move)

        new_move = self.engine.get_best_move()

        if not new_move:
            new_move = self.engine.get_random_move()
            print("random move")

        self.engine.add_move(new_move)
        return new_move

    def get_and_reset_current_logs(self) -> str:
        return ""

    def get_and_reset_all_logs(self) -> str:
        return ""
