from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Callable
import random
import math
from main import Board
from collections import defaultdict


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
        actions = {}
        for a in range(7):
            new_board = deepcopy(board)
            if not new_board.play(a, self.player_id):
                continue
            actions[a] = self.min_player(new_board, p - 1)[0]
        max_u = max(actions.values())
        return max_u, random.choice([k for k, v in actions.items() if v == max_u])

    def min_player(self, n: Board, p: int) -> tuple[int, int]:
        if n.check_win() or p == 0:
            return self.evaluate(n), None
        actions = {}
        for a in range(7):
            new_board = deepcopy(n)
            if not new_board.play(a, self.player_id % 2 + 1):
                continue
            actions[a] = self.max_player(new_board, p - 1)[0]
        min_u = min(actions.values())
        return min_u, random.choice([k for k, v in actions.items() if v == min_u])


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


class UCT(Algorithm):
    def __init__(self, state: Board, player_id: int, parent=None, parent_action=None):
        self.player_id = player_id
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.action = None
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = list(range(7))

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def run(self, **kwargs) -> int:
        return self.uctSearch(kwargs["board"]).action

    def uctSearch(self, s0: Board) -> "UCT":
        number_of_simulations = 100

        for _ in range(number_of_simulations):
            v = self.treePolicy(s0)
            reward = v.rollout()
            v.backpropagate(reward)
        return self.best_child(c_param=0.0)

    def treePolicy(self, v: Board) -> "UCT":
        current = self
        while not v.check_win():
            if not current.is_fully_expanded():
                return current.expand(v)
            else:
                current = current.best_child()
        return current

    def expand(self, v: Board) -> "UCT":
        action = self._untried_actions.pop()
        next_state = deepcopy(v)
        next_state.play(action, self.player_id)
        child_node = UCT(
            next_state, self.player_id % 2 + 1, parent=self, parent_action=action
        )
        child_node.action = action

        self.children.append(child_node)
        return child_node

    def rollout(self) -> int:
        while not self.state.check_win():
            action = random.randint(0, 6)
            if not self.state.play(action, self.player_id):
                continue
        return 1 if self.state.check_win() else -1

    def backpropagate(self, result: int) -> None:
        self._number_of_visits += 1
        self._results[result] += 1
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self) -> bool:
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1) -> "UCT":
        choices_weights = [
            (c.q() / c._number_of_visits)
            + c_param
            * math.sqrt((2 * math.log(self._number_of_visits) / c._number_of_visits))
            for c in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def rollout_policy(self, possibleMoves: list) -> int:
        return possibleMoves[random.randint(len(possibleMoves))]
