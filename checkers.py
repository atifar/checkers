"""Checkers game"""

import os

# Display representation of "reachable" squares
PIECE_DISP = {
    "wm": " \u26aa ",
    "wk": " \u26c1 ",
    "bm": " \u26ab ",
    "bk": " \u26c3 ",
    "": "   "
}
# Display representation of "non-reachable" white squares
WH_SQ = "\u2591" * 3
# Display representation of box lines
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
    while True:
        curr_player = game.black_name if game.blacks_turn else \
            game.white_name
        move = game.get_player_move_from()
        if move == 'r':
            game.draw_offered = False
            print("{} has resigned. Game over!".format(curr_player))
            break
        elif move == 'd':
            if game.draw_offered:
                print("Game ended in a draw!")
                break
            else:
                game.draw_offered = True
                game.move_msg = "{} is offering a draw.".format(curr_player)
                game.switch_to_opponent()
                continue
        # Here move contains the number of a square. Convert it to integer in
        # internal representation
        square = int(move) - 1
        game.draw_offered = False
        # Validate that the 'square' piece is legal to play; Return True/False,
        # and set move_msg in validate()
        if game.board.validate_piece(game, square):
            while True:
                move_to = game.get_player_move_to()  # Return legal move_to
                # Perform move, including capture, crowning
                # if turn is over, reset piece_to_move, move_msg, move_to, then
                #       break out of loop
                # else set piece_to_move = move_to, continue with next loop
        else:
            # move_msg was set by validate
            break
        # Turn has been switched by this point.
        if game.board.is_game_over(game):
            # Display winner and exit loop
            break
    print("Good bye!")


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
        self.move_msg = ''
        self.draw_offered = False
        self.game_piece_to_move = None

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

    def get_player_move_from(self):
        """Gets player's next move

        Displays the game board then prints any error message from previous
        input validation, then prompts for player input. Accepts only 'r', 'd'
        or 1-32 input, otherwise reprompts. Returns accepted input, and resets
        error message to empty string.
        """
        valid_moves = [str(i) for i in range(1, 33)]
        valid_moves.extend(['r', 'd'])
        curr_player = self.black_name if self.blacks_turn else self.white_name
        while True:
            self.board.display_board(self)
            print("{}, it is your turn.".format(curr_player))
            print(self.move_msg)
            prompt = "What is your next move?\n" +\
                "(r)esign | (d)raw | 1 - 32 to pick a piece to move -> "
            move = input(prompt).lower()
            if move in valid_moves:
                self.move_msg = ''
                return move
            self.move_msg = 'Invalid entry. Try again!'

    def get_available_moves(self):
        """Return all available moves for current player

        The return value is a list of movable pieces, whose elements are tuples
        of the form (piece_index<int>, can_piece_jump?<boolean>).
        """
        moves = []
        active_pieces = ("bm", "bk") if self.blacks_turn else ("wm", "wk")
        opponents = ("wm", "wk") if self.blacks_turn else ("bm", "bk")
        for idx, piece in enumerate(self.board.squares):
            # Check only squares with pieces belonging to the current player
            if piece in active_pieces:
                if self.board.can_jump(idx, opponents):
                    moves.append((idx, True))
                elif self.board.can_move(idx):
                    moves.append((idx, False))
        return moves

    def switch_to_opponent(self):
        """Switches to other player's turn"""
        self.blacks_turn = not self.blacks_turn
        self.move_msg = ''
        self.piece_to_move = None


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
        empty_sq = WH_SQ + BOX["vb"]
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

    def jump_room_exists(self, square_idx, direction):
        """Checks if there is room on the board to jump in given direction

        Diagonal direction (value: meaning) are as follows (internal square
        representation - 0-31):
        'NW': toward corner of board near square 0
        'NE': toward corner of board near square 3
        'SW': toward corner of board near square 28
        'SE': toward corner of board near square 31
        Returns True if there is an empty square diagonally two squares
        away in the given direction, otherwise returns False.
        """
        if direction == 'NW':
            if square_idx >= 9 and square_idx % 4:
                return self.get_square(square_idx-9) == ""
            else:
                return False
        elif direction == 'NE':
            if square_idx >= 8 and (square_idx+1) % 4:
                return self.get_square(square_idx-7) == ""
            else:
                return False
        elif direction == 'SW':
            if square_idx <= 23 and square_idx % 4:
                return self.get_square(square_idx+7) == ""
            else:
                return False
        else:
            if square_idx <= 22 and (square_idx+1) % 4:
                return self.get_square(square_idx+9) == ""
            else:
                return False

    def can_jump(self, square_idx, opponents):
        """Determine if the piece on given square can jump

        Return True if piece at square_idx has an available jump, otherwise
        return False. This function assumes that it's only called if the
        piece at square_idx belongs to the player in the current turn.
        """
        if self.get_square(square_idx) in ("bm", "bk", "wk"):
            # "bm", "bk" or "wk" can move in southerly direction
            # Can jump in SE direction?
            if self.jump_room_exists(square_idx, "SE"):
                diag_offs = 4 if (square_idx//4) % 2 else 5
                if self.get_square(square_idx+diag_offs) in opponents:
                    return True  # Jump available in SE direction
            # Can jump in SW direction?
            if self.jump_room_exists(square_idx, "SW"):
                diag_offs = 3 if (square_idx//4) % 2 else 4
                if self.get_square(square_idx+diag_offs) in opponents:
                    return True  # Jump available in SW direction
        if self.get_square(square_idx) in ("bk", "wm", "wk"):
            # "bk", "wm" or "wk" can move in northerly direction
            # Can jump in NE direction?
            if self.jump_room_exists(square_idx, "NE"):
                diag_offs = -4 if (square_idx//4) % 2 else -3
                if self.get_square(square_idx+diag_offs) in opponents:
                    return True  # Jump available in NE direction
            # Can jump in NW direction?
            if self.jump_room_exists(square_idx, "NW"):
                diag_offs = -5 if (square_idx//4) % 2 else -4
                if self.get_square(square_idx+diag_offs) in opponents:
                    return True  # Jump available in NW direction
        else:
            return False  # No jump available in any direction

    def can_move(self, square_idx):
        """Determine if the piece on given square can move

        Return True if piece at square_idx has an available simple move,
        otherwise return False. This function assumes that it's only called
        if the piece at square_idx belongs to the player in the current turn.
        """
        if self.get_square(square_idx) in ("bm", "bk", "wk"):
            # "bm", "bk" or "wk" can move in southerly direction
            # Can move in SE direction?
            if square_idx <= 26 and square_idx not in (3, 11, 19):
                diag_offs = 4 if (square_idx//4) % 2 else 5
                if self.get_square(square_idx+diag_offs) == "":
                    return True  # Simple move available in SE direction
            # Can move in SW direction?
            if square_idx <= 27 and square_idx not in (4, 12, 20):
                diag_offs = 3 if (square_idx//4) % 2 else 4
                if self.get_square(square_idx+diag_offs) == "":
                    return True  # Simple move available in SW direction
        if self.get_square(square_idx) in ("bk", "wm", "wk"):
            # "bk", "wm" or "wk" can move in northerly direction
            # Can move in NE direction?
            if square_idx >= 4 and square_idx not in (11, 19, 27):
                diag_offs = -4 if (square_idx//4) % 2 else -3
                if self.get_square(square_idx+diag_offs) == "":
                    return True  # Simple move available in NE direction
            # Can move in NW direction?
            if square_idx >= 5 and square_idx not in (12, 20, 28):
                diag_offs = -5 if (square_idx//4) % 2 else -4
                if self.get_square(square_idx+diag_offs) == "":
                    return True  # Simple move available in NW direction
        else:
            return False  # No simple move available in any direction

    def validate_piece(self, game, piece):
        """Validate that moving the selected piece is legal.

        If 'piece' either has an available jump, or it has an available simple
        move but no other piece of the current player has an available jump,
        then the move is valid. For a valid move this function returns True,
        and clears the message for the next move. For an invalid message the
        function returns False, and sets the appropriate message.
        """
        pass

    def display_board(self, game):
        """Display game board with player names after clearing the screen"""

        # Define elements for drawing the board
        hbx3 = BOX["hb"] * 3
        top = BOX["ul"] + (hbx3+BOX["nt"]) * 7 + hbx3 + BOX["ur"]
        mid = BOX["wt"] + (hbx3+BOX["cc"]) * 7 + hbx3 + BOX["et"]
        bot = BOX["ll"] + (hbx3+BOX["st"]) * 7 + hbx3 + BOX["lr"]
        # Construct the board
        board_view = top + "\n"
        for row in range(1, 8):
            board_view = board_view + self.get_row(row) + "\n" + mid + "\n"
        board_view = board_view + self.get_row(8) + "\n" + bot
        # Clear the screen and display the player names and board
        os.system('clear')
        print("Black: {}".format(game.black_name))
        print(board_view)
        print("White: {}\n".format(game.white_name))

if __name__ == "__main__":
    game = Checkers()
    play_game(game)
