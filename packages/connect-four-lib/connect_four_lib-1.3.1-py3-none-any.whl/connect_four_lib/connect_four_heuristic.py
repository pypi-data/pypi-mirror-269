from functools import cache

from connect_four_lib.config import HEURISTIC_BASE, MAX_HEURISTIC


class ConnectFourHeuristic:
    @cache
    @staticmethod
    def __get_point(column: int, row: int, board: list[list[int]]) -> int:
        if not 0 <= column < len(board) or not 0 <= row < len(board[0]):
            return -1

        return board[column][row]

    @staticmethod
    def __get_windows(
        column: int, row: int, board: tuple[tuple[int, ...], ...]
    ) -> list[int]:
        windows = []

        windows.append(
            tuple(
                ConnectFourHeuristic.__get_point(column, row + i, board)
                for i in range(4)
            )
        )
        windows.append(
            tuple(
                ConnectFourHeuristic.__get_point(column + i, row, board)
                for i in range(4)
            )
        )
        windows.append(
            tuple(
                ConnectFourHeuristic.__get_point(column + i, row + i, board)
                for i in range(4)
            )
        )
        windows.append(
            tuple(
                ConnectFourHeuristic.__get_point(column + i, row - i, board)
                for i in range(4)
            )
        )

        return windows

    @cache
    @staticmethod
    def _evaluate_window(window: list[int], color: int) -> int:
        points = window.count(color)
        empty_points = window.count(0)

        evaluation = 0

        if points == 4:
            return MAX_HEURISTIC

        if points + empty_points == 4:
            evaluation = HEURISTIC_BASE**points

        return evaluation

    @staticmethod
    def evaluate(board: list[list[int]], color: int) -> int:
        windows = []
        hashable_board = tuple(tuple(column) for column in board)

        for column in range(len(board)):
            for row in range(len(board[0])):
                windows.extend(
                    ConnectFourHeuristic.__get_windows(column, row, hashable_board)
                )

        evaluation = sum(
            ConnectFourHeuristic._evaluate_window(window, color)
            - ConnectFourHeuristic._evaluate_window(window, 3 - color)
            for window in windows
        )

        if evaluation >= 5000:
            evaluation = MAX_HEURISTIC
        elif evaluation <= -5000:
            evaluation = -MAX_HEURISTIC

        return evaluation
