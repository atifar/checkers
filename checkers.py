"""Checkers game"""

import os

PIECE_DISP = {
    "wm": " \u26aa ",
    "wk": " \u26c1 ",
    "bm": " \u26ab ",
    "bk": " \u26c3 ",
    "": "\u2591" * 3
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


def play_game(game):
    """Run the checkers game

    This is the entry function that runs the entire game.
    """
    game.show_rules()
    game.get_player_names()
    os.system('clear')
    game.board.display_board(game.black_name, game.white_name)


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

    @staticmethod
    def show_rules():
        """Display game rules"""
        rules = """
Welcome to this awesome checkers game!


The game rules are as follows:

Two players participate in the game. Each has a starting set of 12
game pieces (men), one set white and the other black. Each player's
men are initially placed on the 12 dark squares of the board
closest to them. The player with the black pieces starts the game,
then the players take turns moving one piece each turn.

There are two types of moves, a simple move and a jump. for both
types of moves an uncrowned piece (man) may only move forward,
while a crowned piece (king) may move in any diagonal direction.
Initially all pieces are uncrowned. A piece that reaches the edge
of the board (moving in the forward direction) becomes crowned
(king).

As simple move consists of sliding a piece one square diagonally
to an adjacent dark square. After a simple move the player's turn
ends.

A jump is a move from a square diagonally adjacent to an opponent's
piece to an empty dark square immediately beyond it, in the same
direction (jumping over the opponent's piece). A jumped piece is
considered captured, and is removed from the board. If after a
jump another jump is possible with the same piece, it must be
taken. If more than one multiple-jump move is possible, the
player may choose among them.

Jumping is mandatory. If both types of moves are possible, a jump
must be taken. A player must continue the jump sequence until no
further jump is available, at which point the turn ends.

A player wins by capturing all of the opponent's pieces or by
leaving the opponent with no legal move. The game may also end
in a draw if neither side can force a win, and one side is
offering a draw which the opponent accepts.
        """
        print(rules)

    def get_player_names(self):
        """Prompt for player names"""
        for color in ('black', 'white'):
            prompt = "Player for {}, please type in your name: ".format(color)
            while True:
                name = input(prompt)
                if name:
                    if color == 'black':
                        self.black_name = name
                    else:
                        self.white_name = name
                    print("Thank you!")
                    break


class Board:
    """Game board for checkers

    The reachable squares on the board are numbered from 1 to 32, which are
    represented in the self.squares[0-31] list containing string values.
    Valid string values are those of the keys of the PIECE_DISP dictionary.

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
        self.squares = ["bm" for _ in range(12)]
        # 8 blank squares on 12-19
        self.squares.extend(["" for _ in range(8)])
        # 12 initial black men on squares 20-31
        self.squares.extend(["wm" for _ in range(12)])

    def get_board_stats(self):
        """Return stats of pieces and empty squares on the board"""
        stats = dict.fromkeys(PIECE_DISP.keys(), 0)
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
        empty_sq = PIECE_DISP[""] + BOX["vb"]
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
        # Reachable squares for the current row in Portable Draughts Notation
        p_d_notation = "<{}-{}>".format(first_idx + 1, first_idx + 4)
        return row_out + p_d_notation
        # return row_out

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
    play_game(game)
