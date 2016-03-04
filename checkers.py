"""Checkers game"""

import os

# Display representation of "reachable" squares
PIECE_DISP = {
    "wm": " \u26aa ",
    "wk": " \u265a ",
    "bm": " \u26ab ",
    "bk": " \u2654 ",
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
        # Prompt for player input
        move = game.get_player_move_from()
        if move == 'r':
            print("{} has resigned. Game over!".format(curr_player))
            break
        elif move == 'd':
            game.move_msg = "{} is offering a draw.".format(curr_player)
            if game.draw_accepted():
                print("Game ended in a draw!")
                break
            else:
                # Clear move message before the next move
                game.move_msg = ""
                continue
        # Here move contains the number of a square. Convert it to integer in
        # internal representation
        square = int(move) - 1
        # Validate that the piece on the selected square is legal to play
        if game.validate_pick(square):
            # Prompt player for square to move to
            while True:
                move_to = game.get_player_move_to()
                # Convert it to internal representation
                square = int(move_to) - 1
                # Validate that the selected square is legal to move to
                if game.validate_move_to(square):
                    game.board.move_piece_to(game, square)
                else:
                    continue
                if game.turn_is_complete(square):
                    # It was a simple move or no more jumps are available
                    game.game_piece_to_move = None
                    game.must_jump = False
                    break
                # More jumps are available, which must be taken
                game.game_piece_to_move = square
                continue
        else:
            # Return to the top of the game loop to prompt the player again
            continue
        # The current player's turn has completed. Switch turns.
        game.switch_turns()
        if game.has_player_lost():
            game.board.display_board(game)
            winner = game.white_name if game.blacks_turn else game.black_name
            print("Congratulations {}! You have won.".format(winner))
            break
    # Game over
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
        self.game_piece_to_move = None
        self.must_jump = False

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
row, aka kings row, (moving in the forward direction) becomes crowned
(promoted to a king).

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
further jump is available, at which point the turn ends. Jumping
into the kings row always ends the turn.

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

    def draw_accepted(self):
        """Get opponent's answer to draw offer and return it

        Return True if draw was accepted, otherwise return False.
        """
        self.board.display_board(self)
        opponent = self.white_name if self.blacks_turn else self.black_name
        print("{}, ".format(opponent) + self.move_msg + "\n")
        prompt = "Enter 'y' to accept the draw or anything else" +\
            " to reject it.\n -> "
        return input(prompt).lower() == "y"

    def get_player_move_from(self):
        """Get player's next move

        Display the game board then print any error message from previous
        input validation and prompt for player input. Accept only 'r', 'd'
        or 1-32 input, otherwise reprompt. Return accepted input, and reset
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

    def get_player_move_to(self):
        """Get player's selection of where to move picked-up piece.

        Display the game board then print any error message from previous
        input validation and prompt for player input. Accept only a square
        (1-32) as input, otherwise reprompt. Return accepted input.
        """
        valid_moves = [str(i) for i in range(1, 33)]
        curr_player = self.black_name if self.blacks_turn else self.white_name
        input_message = ''
        while True:
            self.board.display_board(self)
            print("{}, it is your turn.".format(curr_player))
            print(self.move_msg)
            print(input_message)
            prompt = "Where do you want to move this piece?\n" +\
                "1 - 32 to pick a square to move to -> "
            move = input(prompt).lower()
            if move in valid_moves:
                return move
            input_message = 'Invalid entry. Try again!'

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
                if self.board.valid_jumps(idx, opponents):
                    moves.append((idx, True))
                elif self.board.valid_moves(idx):
                    moves.append((idx, False))
        return moves

    def square_is_empty_or_has_opponents_piece(self, square):
        """Check if square has no legal piece to move

        If the selected square has no or the opponent's piece on it, set
        message and return True. Otherwise reset message to empty string
        and return False.
        """
        wrong_pieces = ("wm", "wk", "") if self.blacks_turn else \
            ("bm", "bk", "")
        if self.board.get_square(square) in wrong_pieces:
            self.move_msg = "You don't have a piece on that square to move."
            return True
        self.move_msg = ""
        return False

    def available_jump_or_move_exists(self, square, moves):
        """Check if the piece on square can jump or make a simple move

        If the piece on 'square' either has an available jump, or it has an
        available simple move but no other piece of the current player has
        an available jump, then set move message, set the game_piece_to_move
        and must_jump attributes and return True. Otherwise only set the move
        message to indicate why the selected piece has no legal move, and
        return False.
        """
        # Selected piece has available jump
        if tuple((square, True)) in moves:
            # Use standard square notation in message
            self.move_msg = "Picked up piece from {}.".format(square+1)
            self.game_piece_to_move = square
            self.must_jump = True
            return True
        # Selected piece has available simple move
        elif tuple((square, False)) in moves:
            # No other piece has available jump
            if any([jump for sq, jump in moves]) is False:
                # Use standard square notation in message
                self.move_msg = "Picked up piece from {}.".format(square+1)
                self.game_piece_to_move = square
                self.must_jump = False
                return True
            else:
                self.move_msg = "You cannot move piece from {}.".format(
                    square+1) + " Take available jump."
                return False
        # No legal jump or move (use standard square notation)
        self.move_msg = "The piece from {} has no legal move.".format(square+1)
        return False

    def validate_pick(self, square):
        """Validate that moving the piece from the selected square is legal.

        Return False and set the message accordingly if the square is empty
        or if one of the opponents' pieces is on it. If the piece on the
        selected square either has an available jump or it has an available
        simple move while no other piece of the current player has an available
        jump, then return True. Also return False if the selected piece
        has no available jump or move.

        When this function exits, the following instance attributes have been
        set to appropriate values: move_msg, game_piece_to_move, must_jump.
        """
        if self.square_is_empty_or_has_opponents_piece(square):
            return False
        moves = self.get_available_moves()
        if self.available_jump_or_move_exists(square, moves):
            return True
        return False

    def validate_move_to(self, square):
        """Validate that the selected square is legal to move to.

        Return True if selected move is legal, otherwise return False.
        """
        # Jump must be taken
        if self.must_jump:
            opponents = ("wm", "wk") if self.blacks_turn else ("bm", "bk")
            if square in self.board.valid_jumps(self.game_piece_to_move,
                                                opponents):
                return True
            else:
                self.move_msg = "The piece from {} must jump.".format(
                    self.game_piece_to_move+1)
                return False
        # No jump, so a simple move must be taken
        else:
            if square in self.board.valid_moves(self.game_piece_to_move):
                return True
            else:
                self.move_msg = "Invalid move from {}.".format(
                    self.game_piece_to_move+1) + " Try again!"
                return False

    def turn_is_complete(self, square):
        """Determine if the current turn is complete

        After a simple move the current turn is complete. After a jump if
        the jumping piece has no further jump available, then the turn is
        complete. Return True if the current turn is complete, otherwise
        return False.
        """
        # After a simple move (or jumping into the kings row)
        if not self.must_jump:
            return True
        # After a jump check if a further jump is available
        moves = self.get_available_moves()
        if tuple((square, True)) in moves:
            self.move_msg = "The piece from {} must jump.".format(square+1)
            return False
        else:
            return True

    def has_player_lost(self):
        """Check if the current player has any piece to play.

        Return True if the current player has no piece left or none of
        the remaining pieces have available moves or jumps. Otherwise
        return False.
        """
        board_stats = self.board.get_board_stats()
        # Does player have no piece left on the board?
        if (self.blacks_turn and board_stats["bm"]+board_stats["bk"] == 0 or
            not self.blacks_turn and board_stats["wm"]+board_stats["wk"] == 0):
            return True
        # Does the current player has any piece to play?
        return not self.get_available_moves()

    def switch_turns(self):
        """Switches to other player's turn"""
        self.blacks_turn = not self.blacks_turn
        self.move_msg = ''
        self.game_piece_to_move = None
        self.must_jump = False


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

    def valid_jumps(self, square, opponents):
        """Find all legal jumps for the piece on square

        Return the list of all legal jumps the piece on square.
        """
        jumps = []
        if self.get_square(square) in ("bm", "bk", "wk"):
            # "bm", "bk" or "wk" can move in southerly direction
            # Can jump in SE direction?
            if self.jump_room_exists(square, "SE"):
                diag_offs = 4 if (square//4) % 2 else 5
                if self.get_square(square+diag_offs) in opponents:
                    # Jump offset in SE direction is 9
                    jumps.append(square+9)  # Add available jump
            # Can jump in SW direction?
            if self.jump_room_exists(square, "SW"):
                diag_offs = 3 if (square//4) % 2 else 4
                if self.get_square(square+diag_offs) in opponents:
                    # Jump offset in SW direction is 7
                    jumps.append(square+7)  # Add available jump
        if self.get_square(square) in ("bk", "wm", "wk"):
            # "bk", "wm" or "wk" can move in northerly direction
            # Can jump in NE direction?
            if self.jump_room_exists(square, "NE"):
                diag_offs = -4 if (square//4) % 2 else -3
                if self.get_square(square+diag_offs) in opponents:
                    # Jump offset in NE direction is -7
                    jumps.append(square-7)  # Add available jump
            # Can jump in NW direction?
            if self.jump_room_exists(square, "NW"):
                diag_offs = -5 if (square//4) % 2 else -4
                if self.get_square(square+diag_offs) in opponents:
                    # Jump offset in NW direction is -9
                    jumps.append(square-9)  # Add available jump
        return jumps

    def valid_moves(self, square):
        """Find all legal simple moves for the piece on square

        Return the list of all legal simple moves the piece on square.
        """
        moves = []
        if self.get_square(square) in ("bm", "bk", "wk"):
            # "bm", "bk" or "wk" can move in southerly direction
            # Can move in SE direction?
            if square <= 26 and square not in (3, 11, 19):
                diag_offs = 4 if (square//4) % 2 else 5
                if self.get_square(square+diag_offs) == "":
                    moves.append(square+diag_offs)  # Add available move
            # Can move in SW direction?
            if square <= 27 and square not in (4, 12, 20):
                diag_offs = 3 if (square//4) % 2 else 4
                if self.get_square(square+diag_offs) == "":
                    moves.append(square+diag_offs)  # Add available move
        if self.get_square(square) in ("bk", "wm", "wk"):
            # "bk", "wm" or "wk" can move in northerly direction
            # Can move in NE direction?
            if square >= 4 and square not in (11, 19, 27):
                diag_offs = -4 if (square//4) % 2 else -3
                if self.get_square(square+diag_offs) == "":
                    moves.append(square+diag_offs)  # Add available move
            # Can move in NW direction?
            if square >= 5 and square not in (12, 20, 28):
                diag_offs = -5 if (square//4) % 2 else -4
                if self.get_square(square+diag_offs) == "":
                    moves.append(square+diag_offs)  # Add available move
        return moves

    def move_piece_to(self, game, square):
        """Make the selected move

        Move the selected piece to the destination square, and crown it if
        necessary. If it was a jump, remove the captured piece.

        NOTE: Jumping into the kings row ends the turn. This is enforced by
        setting the must_jump instance attribute to False.
        """
        # Move the current player's piece
        self.squares[square] = self.squares[game.game_piece_to_move]
        self.squares[game.game_piece_to_move] = ""
        # If current player's piece jumped, remove opponent's captured piece
        if game.must_jump:
            diag_jump_offs = {
                -9: (-4, -5),  # NW diagonal offsets
                -7: (-3, -4),  # NE diagonal offsets
                7: (4, 3),  # SW diagonal offsets
                9: (5, 4)  # SE diagonal offsets
            }
            jump_offs = square - game.game_piece_to_move
            even_odd_row = (game.game_piece_to_move//4) % 2
            captured_offs = diag_jump_offs[jump_offs][even_odd_row]
            self.squares[game.game_piece_to_move+captured_offs] = ""
        # Crown destination piece if appropriate
        if game.blacks_turn:
            if square > 27:
                self.squares[square] = "bk"
                # Jumping into the kings row ends the turn
                game.must_jump = False
        else:
            if square < 4:
                self.squares[square] = "wk"
                # Jumping into the kings row ends the turn
                game.must_jump = False

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
