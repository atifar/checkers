"""Unit tests for checkers game"""

from io import StringIO
from unittest.mock import patch
import pytest
from .checkers import Checkers, Board
from .checkers import PIECE_DISP, BOX, WH_SQ

# Constants used in testing the board display functions
VB = BOX["vb"]  # Vertical bar
HB = BOX["hb"]  # Horizontal bar
UL = BOX["ul"]  # Upper left corner
UR = BOX["ur"]  # Upper right corner
LL = BOX["ll"]  # Lower left corner
LR = BOX["lr"]  # Lower right corner
NT = BOX["nt"]  # North tee
ST = BOX["st"]  # South tee
ET = BOX["et"]  # East tee
WT = BOX["wt"]  # West tee
CC = BOX["cc"]  # Center cross
H3 = HB * 3  # 3 horizontal bars
MID = WT + (H3+CC) * 7 + H3 + ET  # Line between rows of the board

ES = "   "  # Empty black square
WSQ = VB + WH_SQ + VB  # White square with vb-s on each side
WM = PIECE_DISP["wm"]  # White man
WK = PIECE_DISP["wk"]  # White king
BM = PIECE_DISP["bm"]  # Black man
BK = PIECE_DISP["bk"]  # Black king

PDN1 = "<1-4>"  # Portable Draughts Notation - Row 1
PDN2 = "<5-8>"  # Portable Draughts Notation - Row 2
PDN3 = "<9-12>"  # Portable Draughts Notation - Row 3
PDN4 = "<13-16>"  # Portable Draughts Notation - Row 4
PDN5 = "<17-20>"  # Portable Draughts Notation - Row 5
PDN6 = "<21-24>"  # Portable Draughts Notation - Row 6
PDN7 = "<25-28>"  # Portable Draughts Notation - Row 7
PDN8 = "<29-32>"  # Portable Draughts Notation - Row 8


def update_board(board, updates):
    """Return board with updated squares

    Updates is a two-tuple. The first member is the square index in
    internal representation (0-31). The second is the string value to
    update the square with.

    Reachable board square index map:
    -------------------------
    |  |0 |  |1 |  |2 |  |3 |
    -------------------------
    |4 |  |5 |  |6 |  |7 |  |
    -------------------------
    |  |8 |  |9 |  |10|  |11|
    -------------------------
    |12|  |13|  |14|  |15|  |
    -------------------------
    |  |16|  |17|  |18|  |19|
    -------------------------
    |20|  |21|  |22|  |23|  |
    -------------------------
    |  |24|  |25|  |26|  |27|
    -------------------------
    |28|  |29|  |30|  |31|  |
    -------------------------
    """
    for index, value in updates:
        board.squares[index] = value


###################################
# #### Board class tests
###################################
class TestBoardClass:
    @pytest.fixture()
    def game_board(self):
        return Board()

    @pytest.fixture()
    def empty_board(self, game_board):
        game_board.squares = ["" for _ in range(32)]
        return game_board

    def test_get_square_returns_stored_value(self, game_board):
        game_board.squares[5] = "Doodly doo"
        assert game_board.get_square(5) == "Doodly doo"

    def test_get_square_invalid_index(self, game_board):
        pytest.raises(IndexError, game_board.get_square, 32)

    def test_board_initial_piece_locations(self, game_board):
        for index in range(12):
            assert game_board.get_square(index) == "bm"
        for index in range(12, 20):
            assert game_board.get_square(index) == ""
        for index in range(20, 32):
            assert game_board.get_square(index) == "wm"

    def test_get_board_stats(self, game_board):
        updates = [(7, ""), (9, ""), (15, "wk"), (19, "bm"), (21, "")]
        update_board(game_board, updates)
        stats = game_board.get_board_stats()
        assert stats["wk"] == 1, "incorrect number of white kings"
        assert stats["wm"] == 11, "incorrect number of white men"
        assert stats["bk"] == 0, "incorrect number of black kings"
        assert stats["bm"] == 11, "incorrect number of black men"
        assert stats[""] == 9, "incorrect number of empty squares"

    def test_get_even_row(self, game_board):
        row = 4
        updates = [(13, "bm"), (14, "wk"), (15, "bk")]
        update_board(game_board, updates)
        # Build string for updated row
        correct_line = (VB + ES + WSQ + BM + WSQ + WK + WSQ + BK +
                        WSQ + PDN4)
        generated_line = game_board.get_row(row)
        assert len(correct_line) == len(generated_line), \
            "string lengths don't match"
        assert correct_line == generated_line, \
            "generated_line doesn't match expected one"

    def test_get_odd_row(self, game_board):
        row = 7
        updates = [(24, "bm"), (26, "wk"), (27, "bk")]
        update_board(game_board, updates)
        # Build string for updated row
        correct_line = (WSQ + BM + WSQ + WM + WSQ + WK + WSQ + BK +
                        VB + PDN7)
        generated_line = game_board.get_row(row)
        assert len(correct_line) == len(generated_line), \
            "string lengths don't match"
        assert correct_line == generated_line, \
            "generated_line doesn't match expected one"

    # Need comprehensive coverage for jump_room_exists()
    def test_jump_room_exists(self, empty_board):
        updates = [(8, "bm"), (13, "bm"), (17, "bk")]
        update_board(empty_board, updates)
        assert empty_board.jump_room_exists(8, "NE") is True
        assert empty_board.jump_room_exists(8, "SE") is False


###################################
# #### Checkers class tests
###################################
class TestCheckersClass:
    @pytest.fixture()
    def game(self):
        return Checkers()

    @pytest.fixture()
    def initgame(self, game):
        game.black_name = 'Kat'
        game.white_name = 'Rob'
        return game

    @pytest.fixture()
    def emptygame(self, game):
        game.black_name = 'Kat'
        game.white_name = 'Rob'
        # Blank out the game board
        game.board.squares = ["" for _ in range(32)]
        return game

    @patch('builtins.input', side_effect=['Kat', 'Rob'])
    def test_game_creates_initial_board(self, mock_input, game):
        assert game.board, "game did't create the board"

    @patch('builtins.input', side_effect=['Kat', 'Rob'])
    def test_game_updates_default_player_names(self, mock_input, game):
        assert game.black_name == "Peter"
        assert game.white_name == "Amanda"
        game.get_player_names()
        assert game.black_name == "Kat"
        assert game.white_name == "Rob"

    @patch('builtins.input', side_effect=['', 'Kat', '', '', 'Rob'])
    def test_get_player_names_reprompts_on_empty_input(self, mock_input, game):
        assert game.black_name == "Peter"
        assert game.white_name == "Amanda"
        game.get_player_names()
        assert game.black_name == "Kat"
        assert game.white_name == "Rob"

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_board_shows_names_and_sides(
        self,
        mock_stdout,
        initgame
    ):
        initgame.board.display_board(initgame)
        captured_output = mock_stdout.getvalue()
        assert "Black: Kat" in captured_output, \
            "black player was not displayed"
        assert "White: Rob" in captured_output, \
            "white player was not displayed"

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_board_shows_board_correctly(
        self,
        mock_stdout,
        initgame
    ):
        initgame.board.display_board(initgame)
        captured_output = mock_stdout.getvalue()
        # Build expected string that represents the starting board
        board_lines = [
            UL + (H3+NT) * 7 + H3 + UR,
            (WSQ+BM) * 4 + VB + PDN1 + "\n" + MID,
            VB + (BM+WSQ) * 4 + PDN2 + "\n" + MID,
            (WSQ+BM) * 4 + VB + PDN3 + "\n" + MID,
            VB + (ES+WSQ) * 4 + PDN4 + "\n" + MID,
            (WSQ+ES) * 4 + VB + PDN5 + "\n" + MID,
            VB + (WM+WSQ) * 4 + PDN6 + "\n" + MID,
            (WSQ+WM) * 4 + VB + PDN7 + "\n" + MID,
            VB + (WM+WSQ) * 4 + PDN8,
            LL + (H3+ST) * 7 + H3 + LR
        ]
        board = "\n".join(board_lines)
        assert board in captured_output, \
            "starting board display is incorrect"

        # Update a few pieces on the board
        updates = [(23, "bm"), (26, "wk"), (27, "bk")]
        update_board(initgame.board, updates)
        initgame.board.display_board(initgame)
        captured_output = mock_stdout.getvalue()
        board_lines[6] = VB + (WM+WSQ) * 3 + BM + WSQ + PDN6 + "\n" + MID
        board_lines[7] = (WSQ+WM) * 2 + WSQ + WK + WSQ + BK + VB + \
            PDN7 + "\n" + MID
        board = "\n".join(board_lines)
        assert board in captured_output, \
            "updated board display is incorrect"

    def test_get_player_move_from_prints_message_prompt(self, initgame):
        assert initgame.move_msg == ''  # Should be the inital message string
        message = 'It is not legal to move that piece.'
        initgame.move_msg = message
        with patch('builtins.input', side_effect=['r']), \
                patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            initgame.get_player_move_from()
        captured_output = mock_stdout.getvalue()
        assert message in captured_output

    @pytest.mark.parametrize("move, expected", [
        ('4', '4'),
        ('r', 'r'),
        ('R', 'r'),
        ('d', 'd')
    ])
    def test_get_player_move_from_returns_valid_input(
        self,
        move,
        expected,
        initgame
    ):
        with patch('builtins.input', side_effect=[move]):
            return_move = initgame.get_player_move_from()
        assert return_move == expected, \
            "valid 'player_move_from' was not returned"

    def test_get_player_move_from_reprompts_invalid_input(self, initgame):
        with patch('builtins.input', side_effect=['-1', '98', 'z', 'we', '8']):
            return_move = initgame.get_player_move_from()
        assert return_move == '8', \
            "invalid 'player_move_from' was returned"

    def test_switch_turns_flips_state(self, game):
        game.switch_turns()
        assert game.blacks_turn is False, \
            "it shoud be white's turn"
        game.switch_turns()
        assert game.blacks_turn is True, \
            "it shoud be black's turn"

    def test_switch_turns_resets_instance_attributes(self, game):
        game.move_msg = "This will not stand!"
        game.game_piece_to_move = 12
        game.must_jump = None
        game.switch_turns()
        assert game.move_msg == '', "move_msg should be empty"
        assert game.game_piece_to_move is None, "piece_to_move was not reset"
        assert game.must_jump is False, "must_jump should be False"

    def test_get_available_moves_black_no_move(self, emptygame):
        updates = [(21, "wm"), (24, "wk"), (28, "bk")]
        update_board(emptygame.board, updates)
        assert emptygame.get_available_moves() == []

    def test_get_available_moves_black_simple_move(self, emptygame):
        updates = [(1, "bk"), (21, "wm"), (24, "wk"), (28, "bk")]
        update_board(emptygame.board, updates)
        assert emptygame.get_available_moves() == [(1, False)]

    def test_get_available_moves_white_simple_move(self, emptygame):
        updates = [(16, "bk"), (21, "wm"), (24, "wk"), (28, "bk")]
        update_board(emptygame.board, updates)
        emptygame.blacks_turn = False
        assert emptygame.get_available_moves() == [(21, True), (24, False)]

    # Need to add comprehensive coverage of get_available_moves()
