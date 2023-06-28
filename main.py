class Player:
    def __init__(self, player_id):
        self.player_id = player_id

    def play(self) -> int:
        column = int(input(f"[{self}] >"))
        return column - 1

    def __repr__(self):
        return f"{Board.tokens[self.player_id]} Player {self.player_id}"


class Game:
    def __init__(self):
        from ai import AI  # noqa

        self.board = Board()
        # self.players = [Player(1), Player(2)]
        # self.players = [Player(1), AI(2, self.board)]
        self.players = [AI(1, self.board), AI(2, self.board)]
        self.current_player_id = 0

    def play(self) -> None:
        self.board.print_board()
        while True:
            self.play_turn()
            self.board.print_board()
            if self.board.check_win(self.current_player_id + 1):
                print(f"{self.current_player()} won ! 🎉")
                break
            self.switch_player()

    def play_turn(self) -> None:
        while True:
            column = self.current_player().play()
            if self.board.play(column, self.current_player_id + 1):
                break
            self.board.print_board()

    def current_player(self) -> Player:
        return self.players[self.current_player_id]

    def switch_player(self) -> None:
        self.current_player_id = (self.current_player_id + 1) % 2


class Board:
    tokens = {0: "⚫", 1: "🟡", 2: "🔴"}

    def __init__(self):
        self.board = [[0 for _ in range(7)] for _ in range(6)]

    def print_board(self) -> None:
        print()
        print(" " + " ".join([str(i + 1) for i in range(7)]))
        print(" v" * 7)
        for row in self.board:
            print("".join([Board.tokens[char] for char in row]))

    def play(self, column, player_id) -> bool:
        if self.board[0][column] != 0:
            return False
        for i in range(6):
            if self.board[i][column] != 0:
                i -= 1
                break
        self.board[i][column] = player_id
        return True

    def get_possible_actions(self) -> list[int]:
        return [i for i in range(7) if self.board[0][i] == 0]

    def check_win(self, player_id) -> bool:
        """Check if the current player has won the game"""
        # Horizontal check
        for row in self.board:
            for col in range(4):
                if (
                    row[col]
                    == row[col + 1]
                    == row[col + 2]
                    == row[col + 3]
                    == player_id
                ):
                    return True
        # Vertical check
        for col in range(len(self.board[0])):
            for row in range(3):
                if (
                    self.board[row][col]
                    == self.board[row + 1][col]
                    == self.board[row + 2][col]
                    == self.board[row + 3][col]
                    == player_id
                ):
                    return True

        # Diagonal check
        for row in range(3):
            for col in range(4):
                if (
                    self.board[row][col]
                    == self.board[row + 1][col + 1]
                    == self.board[row + 2][col + 2]
                    == self.board[row + 3][col + 3]
                    == player_id
                ):
                    return True
                if (
                    self.board[row][col + 3]
                    == self.board[row + 1][col + 2]
                    == self.board[row + 2][col + 1]
                    == self.board[row + 3][col]
                    == player_id
                ):
                    return True
        return False

    def is_over(self) -> bool:
        return self.check_win(1) or self.check_win(2)


if __name__ == "__main__":
    game = Game()
    game.play()
