class Game:
    """Connect 4 game class"""

    def __init__(self):
        self.board = Board()
        self.players = [Player(i + 1) for i in range(2)]
        self.current_player_index = 0

    def play(self):
        self.board.print_board()
        while True:
            self.play_turn()
            self.board.print_board()
            if self.check_win():
                print(f"Player {self.current_player_index + 1} won !")
                break
            self.switch_player()

    def play_turn(self):
        column = int(input("Which column do you want to play ?\n> ")) - 1
        self.board.play(column, self.current_player_index)

    def check_win(self):
        return self.board.check_win()

    def switch_player(self):
        self.current_player_index = (self.current_player_index + 1) % 2


class Board:
    """Board class"""

    tokens = {0: "🔘", 1: "🟡", 2: "🔴"}

    def __init__(self):
        self.board = [[0 for i in range(7)] for j in range(6)]

    def print_board(self):
        print(" " + " ".join([str(i + 1) for i in range(7)]))
        print(" v" * 7)
        for row in self.board:
            print("".join([Board.tokens[char] for char in row]))

    def play(self, column, player_index):
        for i in range(6):
            if self.board[i][column] != 0:
                i -= 1
                break
        self.board[i][column] = player_index + 1

    def check_win(self):
        """Check if the current player has won the game"""
        # Horizontal check
        for row in self.board:
            for col in range(4):
                if row[col] == row[col + 1] == row[col + 2] == row[col + 3] != 0:
                    return True
        # Vertical check
        for col in range(len(self.board[0])):
            for row in range(3):
                if (
                    self.board[row][col]
                    == self.board[row + 1][col]
                    == self.board[row + 2][col]
                    == self.board[row + 3][col]
                    != 0
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
                    != 0
                ):
                    return True
                if (
                    self.board[row][col + 3]
                    == self.board[row + 1][col + 2]
                    == self.board[row + 2][col + 1]
                    == self.board[row + 3][col]
                    != 0
                ):
                    return True
        return False


class Player:
    """Player class"""

    def __init__(self, player_number):
        self.player_number = player_number


if __name__ == "__main__":
    game = Game()
    game.play()
