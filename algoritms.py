from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Callable
import random
import math
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
        if board.is_over() or p == 0:
            return self.evaluate(board), None
        actions = {}
        for a in range(7):
            new_board = deepcopy(board)
            if not new_board.play(a, self.player_id):
                continue
            actions[a] = self.min_player(new_board, p - 1)[0]
        max_u = max(actions.values())
        return max_u, random.choice([k for k, v in actions.items() if v == max_u])

    def min_player(self, board: Board, p: int) -> tuple[int, int]:
        if board.is_over() or p == 0:
            return self.evaluate(board), None
        actions = {}
        for a in range(7):
            new_board = deepcopy(board)
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
        if board.is_over() or p == 0:
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
        self, board: Board, p: int, alpha: float, beta: float
    ) -> tuple[int, int]:
        if board.is_over() or p == 0:
            return self.evaluate(board), None
        u = float("inf")
        action = None
        for a in range(7):
            new_board = deepcopy(board)
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


class UCTNode:
    def __init__(self, state: Board, player_id: int, action: int = None, parent=None):
        self.state = state
        self.parent = parent
        self.player_id = player_id
        self.children: list[UCTNode] = []
        self.actions = state.get_possible_actions()
        self.action = action
        self.wins = 0
        self.visits = 0

    def expand(self) -> "UCTNode":
        action = self.actions.pop(random.randint(0, len(self.actions) - 1))
        new_state = deepcopy(self.state)
        new_state.play(action, self.player_id % 2 + 1)
        new_node = UCTNode(new_state, self.player_id % 2 + 1, action, self)
        self.children.append(new_node)
        return new_node

    def best_child(self, c=None):
        return max(self.children, key=lambda node: node.get_uct_score(c))

    def update(self, result):
        self.visits += 1
        self.wins += result

    def get_uct_score(self, c: float = None):
        exploration_factor = c if c else math.sqrt(2)
        if self.visits == 0:
            return float("inf")
        exploitation = self.wins / self.visits
        exploration = exploration_factor * math.sqrt(
            math.log(self.parent.visits) / self.visits
        )
        return exploitation + exploration

    def get_best_action(self) -> int:
        best_child = self.best_child(0)
        return best_child.action


class UCT(Algorithm):
    def __init__(self, player_id):
        self.player_id = player_id

    def run(self, **kwargs) -> int:
        max_iterations = kwargs.get("max_iterations", 1000)
        root = UCTNode(kwargs.get("board"), self.player_id % 2 + 1)
        for _ in range(max_iterations):
            node = self.tree_policy(root)
            delta = self.default_policy(node.state, node.player_id)
            self.backup(node, delta)

        return root.get_best_action()

    def tree_policy(self, node: UCTNode) -> UCTNode:
        while not node.state.is_over():
            if len(node.actions) > 0:
                return node.expand()
            node = node.best_child()
        return node

    def backup(self, node: UCTNode, delta: int):
        while node is not None:
            node.visits += 1
            node.wins += delta
            delta = -delta
            node = node.parent

    def default_policy(self, _state: Board, player_id: int) -> int:
        player = player_id % 2 + 1
        state = deepcopy(_state)
        while not state.is_over():
            actions = state.get_possible_actions()
            if len(actions) == 0:
                break
            action = random.choice(actions)
            state.play(action, player)
            player = player % 2 + 1

        is_self_win = state.check_win(player_id)
        is_oppo_win = state.check_win(player_id % 2 + 1)
        if is_self_win == is_oppo_win:
            return 0
        return 1 if is_self_win else -1
