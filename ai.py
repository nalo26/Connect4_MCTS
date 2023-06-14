import re
from copy import deepcopy

from main import Board, Player
from utils import rotate_board, rows_to_strings, diagonals_board


class AI(Player):
    def __init__(self, player_id, board: Board):
        super().__init__(player_id)
        self.board = board

    def play(self) -> int:
        column = self.minimax(self.board, 4)
        print(f"[{self}] > {column + 1}")
        return column

    def __repr__(self):
        return super().__repr__().replace("Player", "AI 🤖")

    def check(self, board: Board, player_id: int):
        score = 0
        finds = []
        regex = r"pppp|0ppp|p0pp|pp0p|ppp0|00pp|0p0p|0pp0|p00p|p0p0|pp00|000p|00p0|0p00|p000".replace(
            "p", str(player_id)
        )
        horizontal = rows_to_strings(board.board)
        vertical = rows_to_strings(rotate_board(board.board))
        diagonal = rows_to_strings(diagonals_board(board.board))
        for board in (horizontal, vertical, diagonal):
            for row in board:
                str_row = "".join(map(str, row))
                finds.extend(re.findall(regex, str_row))

        for find in finds:
            counts = find.count(str(player_id))
            if counts == 4:
                score += 1000
            elif counts == 3:
                score += 50
            elif counts == 2:
                score += 5
            elif counts == 1:
                score += 1
        return score

    def evaluate(self, board: Board) -> int:
        return self.check(board, self.player_id) - self.check(
            board, self.player_id % 2 + 1
        )

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
