import re

from algoritms import Minimax, AlphaBeta, UCT  # noqa
from main import Board, Player
from utils import diagonals_board, rotate_board, rows_to_strings


class AI(Player):
    def __init__(self, player_id, board: Board):
        super().__init__(player_id)
        self.board = board
        # self.algorithm = Minimax(self.evaluate, self.player_id)
        # self.algorithm = AlphaBeta(self.evaluate, self.player_id)
        self.algorithm = UCT(self.player_id)

    def play(self) -> int:
        # column = self.algorithm.run(board=self.board, max_depth=4)
        column = self.algorithm.run(board=self.board, max_iterations=10000)
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
