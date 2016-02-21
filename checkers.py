"""Checkers game"""

PIECES = {
    "black man": "bm",
    "black king": "bk",
    "white man": "wm",
    "white king": "wk"
}
PIECE_DISP = {
    "wm": " \u26aa ",
    "wk": " \u26c1 ",
    "bm": " \u26ab ",
    "bk": " \u26c3 ",
    "": "   "
}
BOX = {
    "vb": "\u2502",
    "hb": "\u2500",
    "ul": "\u250c",
    "ur": "\u2510",
    "ll": "\u2514",
    "lr": "\u2518",
    "nt": "\u252c",
    "st": "\u2534",
    "et": "\u2524",
    "wt": "\u251c",
    "cc": "\u253c",
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
        """Prompt for player names"""
        self.black_name = input("Player for black, please type in your name: ")
        self.white_name = input("Player for white, please type in your name: ")


class Board:
    """Game board for checkers

    The reachable squares on the board are numbered from 1 to 32, which are
    represented in the self.squares[0-31] list containing string values. An
    empty square corresponds to an empty string, and the other four possibe
    pieces on a square correspond to the values of the PIECES dictionary.

    The standard notation for the reachable squares on the board (1-32) is
    used in the user interface, e.g. in displaying a player's move, and for
    the player to specify a square on the board. The corresponding index
    range (0-31) is used internal to the program.

    The board is organized into eight rows (1-8), with four white and black
    squares each. Odd rows start with a white square. For instance, row 3
    starts with a white square, and contains reachable squares 9-12, which
    are represented by the slice self.squares[8:12].
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
        """Return stats of pieces and empty squares on the board"""
        stats = dict.fromkeys(PIECES.values(), 0)
        stats[""] = 0
        for piece in self.squares:
            stats[piece] += 1
        return stats

    def get_square(self, index):
        """Return the piece on the board by index

        Valid index values are in the 0-31 range, the actual index range of the
        self.squares list."""
        return self.squares[index]

    def get_row(self, row):
        """Return a string representing a board's row"""
        empty_sq = "   " + BOX["vb"]
        first_idx = (row - 1) * 4
        row_out = "".join([
            PIECE_DISP[p] + BOX["vb"] +
            empty_sq for p in self.squares[first_idx:first_idx+3]
        ])
        row_out += PIECE_DISP[self.squares[first_idx+3]]
        if row % 2:
            row_out = BOX["vb"] + empty_sq + row_out + BOX["vb"]
        else:
            row_out = BOX["vb"] + row_out + BOX["vb"] + empty_sq
        return row_out

    def display_board(self, black_name, white_name):
        """Display game board"""

        # Define elements for drawing the board
        hbx3 = BOX["hb"] * 3
        top = BOX["ul"] + (hbx3+BOX["nt"]) * 7 + hbx3 + BOX["ur"]
        mid = BOX["wt"] + (hbx3+BOX["cc"]) * 7 + hbx3 + BOX["et"]
        bot = BOX["ll"] + (hbx3+BOX["st"]) * 7 + hbx3 + BOX["lr"]
        board_view = top + "\n"
        for row in range(1, 8):
            board_view = board_view + self.get_row(row) + "\n" + mid + "\n"
        board_view = board_view + self.get_row(8) + "\n" + bot
        print("Black: {}".format(black_name))
        print(board_view)
        print("White: {}".format(white_name))

if __name__ == "__main__":
    game = Checkers()
    game.play_game()
