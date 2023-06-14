from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Callable

from main import Board


class Algorithm(ABC):
    def __init__(self, evaluate_method: Callable[[Board], int], player_id: int):
        self.evaluate = evaluate_method
        self.player_id = player_id

    @abstractmethod
    def run(self, **kwargs):
        pass


class Minimax(Algorithm):
    def run(self, **kwargs):
        return self.minimax(kwargs["board"], kwargs["max_depth"])

    def minimax(self, root: Board, max_depth: int):
        eval, action = self.max_player(root, max_depth)
        return action

    def max_player(self, board: Board, p: int) -> tuple[int, int]:
        if board.check_win() or p == 0:
            return self.evaluate(board), None
        u = -float("inf")
        action = None
        for a in range(7):
            new_board = deepcopy(board)
            if not new_board.play(a, self.player_id):
                continue
            eval, _ = self.min_player(new_board, p - 1)
            if eval > u:
                u = eval
                action = a
        return u, action

    def min_player(self, n: Board, p: int) -> tuple[int, int]:
        if n.check_win() or p == 0:
            return self.evaluate(n), None
        u = float("inf")
        action = None
        for a in range(7):
            new_board = deepcopy(n)
            if not new_board.play(a, self.player_id % 2 + 1):
                continue
            eval, _ = self.max_player(new_board, p - 1)
            if eval < u:
                u = eval
                action = a
        return u, action


class AlphaBeta(Algorithm):
    def run(self, **kwargs):
        return self.alphaBeta(kwargs["board"], kwargs["max_depth"])

    def alphaBeta(self, root: Board, max_depth: int):
        eval, action = self.max_player(root, max_depth, -float("inf"), float("inf"))
        return action

    def max_player(
        self, board: Board, p: int, alpha: float, beta: float
    ) -> tuple[int, int]:
        if board.check_win() or p == 0:
            return self.evaluate(board), None
        u = -float("inf")
        action = None
        for a in range(7):
            new_board = deepcopy(board)
            if not new_board.play(a, self.player_id):
                continue
            eval, _ = self.min_player(new_board, p - 1, alpha, beta)
            if eval > u:
                u = eval
                action = a
            if u >= beta:
                return u, a
            alpha = max(alpha, u)
        return u, action

    def min_player(
        self, n: Board, p: int, alpha: float, beta: float
    ) -> tuple[int, int]:
        if n.check_win() or p == 0:
            return self.evaluate(n), None
        u = float("inf")
        action = None
        for a in range(7):
            new_board = deepcopy(n)
            if not new_board.play(a, self.player_id % 2 + 1):
                continue
            eval, _ = self.max_player(new_board, p - 1, alpha, beta)
            if eval < u:
                u = eval
                action = a
            if u <= alpha:
                return u, a
            beta = min(beta, u)
        return u, action
