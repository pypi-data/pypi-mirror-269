from duo_game_lib.game_state import GameState
from duo_game_lib.judge import Judge

from connect_four_lib.connect_four_heuristic import ConnectFourHeuristic
from connect_four_lib.point import Point


class ConnectFourJudge(Judge):
    def __init__(
        self,
        moves: list[int] | None = None,
        board: list[list[int]] | None = None,
    ) -> None:
        self.__board: list[list[int]] = board or [([0] * 6) for i in range(7)]
        self.__moves: list[int] = moves or []

    @property
    def board(self) -> list[list[int]]:
        return self.__board

    def get_last_move(self) -> tuple[int, int] | None:
        if not self.__moves:
            return None

        last_move = None
        column = self.__moves[-1]

        for row in range(len(self.__board[column]) - 1, -1, -1):
            if self.__board[column][row] != 0:
                last_move = (column, row)
                break

        return last_move

    def validate(self, move: str) -> GameState:
        state = GameState.CONTINUE

        if not self.__check_valid_move(move):
            return GameState.INVALID

        if not self.__check_illegal_move(int(move)):
            return GameState.ILLEGAL
        return state

    def is_game_over(self) -> GameState:
        state = GameState.CONTINUE
        if self.__is_draw():
            return GameState.DRAW

        if self.__is_win():
            return GameState.WIN

        return state

    def add_move(self, move: str) -> Point:
        column = int(move)
        point = self.__get_position_of_move(move)

        self.__board[point.y][point.x] = (len(self.__moves)) % 2 + 1
        self.__moves.append(column)
        return point

    def remove_last_move(self) -> tuple[int, int]:
        move = self.get_last_move()

        if not move:
            raise IndexError

        self.__moves.pop()
        self.__board[move[0]][move[1]] = 0

        return move

    def get_debug_info(self):
        pass

    def analyze(self, color: int = 1) -> float:
        if self.__is_draw():
            return 0

        return ConnectFourHeuristic.evaluate(self.__board, color)

    def get_all_moves(self) -> list[str]:
        return [str(move) for move in self.__moves]

    def get_valid_moves(self) -> list[int]:
        return [move for move in range(7) if self.__check_illegal_move(move)]

    def __check_valid_move(self, move: str) -> bool:
        move_int = -1
        try:
            move_int = int(move)
        except ValueError:
            return False

        if not 0 <= move_int <= len(self.__board):
            return False

        return True

    def __check_illegal_move(self, move: int) -> bool:
        if self.__board[move][-1] != 0:
            return False

        return True

    def __is_draw(self) -> bool:
        return len(self.__moves) >= 42

    def __is_win(self, point: Point | None = None, next_color=False) -> bool:
        directions = [Point(0, 1), Point(1, 0), Point(1, 1), Point(1, -1)]
        color = self.__calculate_color(next_color)
        last_move = self.get_last_move()

        if not last_move:
            return False

        point = point or Point(last_move[1], last_move[0])

        consecutive_points = [
            1
            + self.__count_consecutive_points(point + direction, direction, color)
            + self.__count_consecutive_points(point - direction, -direction, color)
            for direction in directions
        ]

        return max(consecutive_points) >= 4

    def __calculate_color(self, next_color: bool) -> int:
        color = (len(self.get_all_moves()) + 1) % 2 + 1

        if next_color:
            color = 3 - color

        return color

    def check_win(self, move: str) -> bool:
        return self.__is_win(self.__get_position_of_move(move), False)

    def check_lose(self, move: str) -> bool:
        return self.__is_win(self.__get_position_of_move(move), True)

    def __get_position_of_move(self, move: str) -> Point:
        column = int(move)

        for row, point in enumerate(self.__board[column]):
            if point == 0:
                return Point(row, column)

        return Point(-1, -1)

    def __count_consecutive_points(
        self, point: Point, direction: Point, color: int
    ) -> int:
        if (
            not 0 <= point.x < len(self.__board[0])
            or not 0 <= point.y < len(self.__board)
            or self.__board[point.y][point.x] != color
        ):
            return 0

        return 1 + self.__count_consecutive_points(point + direction, direction, color)
