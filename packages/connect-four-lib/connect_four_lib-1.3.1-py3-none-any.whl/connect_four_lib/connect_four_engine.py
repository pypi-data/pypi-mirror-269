import random
import time

from duo_game_lib.game_state import GameState

from connect_four_lib.config import INFINITY
from connect_four_lib.connect_four_judge import ConnectFourJudge


class ConnectFourEngine:
    def __init__(
        self,
        difficulty: int = 1000,
        judge: ConnectFourJudge | None = None,
        weight: int = 2,
    ) -> None:
        self.__judge: ConnectFourJudge = judge or ConnectFourJudge()
        self.__difficulty: int = difficulty
        self.__start_time: float = 0
        self.__color: int = -1
        self.__weight: int = weight

    def add_move(self, move: str) -> None:
        self.__judge.add_move(move)

    def get_best_move(self) -> str:
        if len(self.__judge.get_all_moves()) <= 2:
            return "3"

        self.__color = len(self.__judge.get_all_moves()) % 2 + 1
        depth = 1
        best_move = self.__judge.get_valid_moves()[0]
        self.__start_time = time.process_time()

        while not self.__is_timeout():
            try:
                best_move = self.__min_max(depth, True)[0]
            except TimeoutError:
                break

            if (
                depth == 1
                and self.__is_critical_move(str(best_move))
                or depth + len(self.__judge.get_all_moves()) >= 42
            ):
                break

            depth += 1

        return str(best_move)

    def get_random_move(self) -> str:
        move = str(random.choice(self.__judge.get_valid_moves()))
        return move

    def __is_timeout(self) -> bool:
        time_used = (time.process_time() - self.__start_time) * 1000
        return time_used >= self.__difficulty

    def __is_critical_move(self, move: str) -> bool:
        return self.__judge.check_win(move) or self.__judge.check_lose(move)

    def __min_max(
        self,
        depth: int,
        maximizing: bool = True,
        alpha: float = -INFINITY,
        beta: float = INFINITY,
    ) -> tuple[int | None, float]:
        """
        Function that performs Minmax algorithm as DFS and returns the evaluation of last move.

        Args:
            move (int): Move to evaluate.
            depth (int): Maximum depth of DFS.
            maximizing (bool): Determines whether to maximize evaluation. Defaults to True.
            alpha (int, optional): Lower bound of the evaluation. Defaults to -INFINITY.
            beta (int, optional): Upper bound of the evaluation. Defaults to INFINITY.

        Returns:
            int: Evaluation of last move.
        """

        if self.__is_timeout():
            raise TimeoutError

        if self.__judge.is_game_over() != GameState.CONTINUE or depth == 0:
            return None, self.__weight**depth * self.__judge.analyze(self.__color)

        best_move = None

        if maximizing:
            best_value = -INFINITY

            for next_move in self.__judge.get_valid_moves():
                self.__judge.add_move(str(next_move))
                new_value = self.__min_max(depth - 1, False, alpha, beta)[1]
                self.__judge.remove_last_move()

                if new_value > best_value:
                    best_value = new_value
                    best_move = next_move
                alpha = max(alpha, best_value)

                if alpha >= beta:
                    break
        else:
            best_value = INFINITY

            for next_move in self.__judge.get_valid_moves():
                self.__judge.add_move(str(next_move))
                new_value = self.__min_max(depth - 1, True, alpha, beta)[1]
                self.__judge.remove_last_move()

                if new_value < best_value:
                    best_value = new_value
                    best_move = next_move
                beta = min(beta, best_value)

                if alpha >= beta:
                    break

        return best_move, best_value
