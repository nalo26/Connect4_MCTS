import re

from main import Game, Player
from utils import rotate_board, rows_to_strings, diagonals_board


class AI(Player):
    def __init__(self, player_id):
        super().__init__(player_id)

    def play(self) -> int:
        return self.minimax(self.game, 3)

    def check(self, game: Game, player_id: int):
        score = 0
        finds = []
        regex = r"pppp|0ppp|p0pp|pp0p|ppp0|00pp|0p0p|0pp0|p00p|p0p0|pp00|000p|00p0|0p00|p000".replace(
            "p", str(player_id)
        )
        horizontal = rows_to_strings(game.board)
        vertical = rows_to_strings(rotate_board(game.board))
        diagonal = rows_to_strings(diagonals_board(game.board))
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

    def evaluate(self, game: Game) -> int:
        return self.check(game, self.player_id) - self.check(
            game, self.player_id % 2 + 1
        )

    def minimax(self, root, max_depth: int):
        eval, action = self.max_player(root, max_depth)
        return action

    def max_player(self, n, p: int) -> tuple[int, int]:
        if n.is_terminal() or p == 0:
            return self.evaluate(n), None
        u = -float("inf")
        action = None
        for a in n.actions():
            n.play(a)
            eval, _ = self.min_player(n, p - 1)
            n.undo(a)
            if eval > u:
                u = eval
                action = a
        return u, action

    def min_player(self, n, p: int) -> tuple[int, int]:
        if n.is_terminal() or p == 0:
            return self.evaluate(n), None
        u = float("inf")
        action = None
        for a in n.actions():
            n.play(a)
            eval, _ = self.max_player(n, p - 1)
            n.undo(a)
            if eval < u:
                u = eval
                action = a
        return u, action
