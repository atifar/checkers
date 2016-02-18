"""Checkers game"""

PIECES = {
    "black man": "bm",
    "black king": "bk",
    "white man": "wm",
    "white king": "wk"
}


class Checkers:
    """Two-player checkers game

    Two players, the first one with dark, the second with light pieces.
    """

    def __init__(self, player_black='Peter', player_white='Amanda'):
        """Construct Checkers instance"""
        self.black_name = player_black
        self.white_name = player_white
        self.board = Board()
        self.blacks_turn = True

    def play_game(self):
        """Run the checkers game

        This is the entry function that runs the entire game.
        """
        self.show_rules()
        self.get_player_names()
        self.board.display_board(self.black_name, self.white_name)

    @staticmethod
    def show_rules():
        """Display game rules"""
        print("Welcome to our checkers game!\n")
        print("Two players participate with a starting set of 12 game pieces",
              "each. The players take turns in moving one piece, and black",
              "starts the game.")  # Finish displaying the rules

    def get_player_names(self):
        """Prompts for player names"""
        self.black_name = input("Player for black, please type in your name: ")
        self.white_name = input("Player for white, please type in your name: ")


class Board:
    """Game board for checkers

    The reachable squares on the board are numbered from 1 to 32, which are
    represented in the self.squares[0-31] list containing string values. An
    empty square corresponds to an empty string, and the other four possibe
    pieces on a square correspond to the values of the PIECES dictionary.
    """

    def __init__(self):
        """Construct game board"""
        # 12 initial black men on squares 0-11
        self.squares = [PIECES["black man"] for _ in range(12)]
        # 8 blank squares on 12-19
        self.squares.extend(["" for _ in range(8)])
        # 12 initial black men on squares 20-31
        self.squares.extend([PIECES["white man"] for _ in range(12)])

    def get_board_stats(self):
        """Returns stats of pieces and empty squares on the board"""
        stats = dict.fromkeys(PIECES.values(), 0)
        stats[""] = 0
        for piece in self.squares:
            stats[piece] += 1
        return stats

    def get_square(self, index):
        """Returns the piece on the board by index

        Valid index values are in the 0-31 range, the actual index range of the
        self.squares list."""
        return self.squares[index]

    def display_board(self, black_name, white_name):
        print("{} plays with the black pieces.".format(black_name))
        print("{} plays with the white pieces.".format(white_name))
