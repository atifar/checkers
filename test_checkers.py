"""Unit tests for checkers game"""

from copy import copy
from io import StringIO
from unittest.mock import patch
import pytest
from .checkers import Checkers, Board, play_game
from .checkers import PIECE_DISP, BOX

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

ES = PIECE_DISP[""]  # Empty square
WH_SQ = VB + ES + VB  # White square with vb-s on each side
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


###################################
# #### Board class tests
###################################
class TestBoardClass:
    @pytest.fixture()
    def game_board(self):
        return Board()

    @staticmethod
    def update_board(board, updates):
        """Return copy of board with updated squares

        updates is a two-tuple. The first member is the square index in
        internal representation (0-31). The second is the string value to
        update the square with.
        """
        board_copy = copy(board)
        for index, value in updates:
            board_copy.squares[index] = value
        return board_copy

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
        game_board = self.update_board(game_board, updates)
        stats = game_board.get_board_stats()
        assert stats["wk"] == 1, "incorrect number of white kings"
        assert stats["wm"] == 11, "incorrect number of white men"
        assert stats["bk"] == 0, "incorrect number of black kings"
        assert stats["bm"] == 11, "incorrect number of black men"
        assert stats[""] == 9, "incorrect number of empty squares"

    def test_get_even_row(self, game_board):
        row = 4
        updates = [(13, "bm"), (14, "wk"), (15, "bk")]
        game_board = self.update_board(game_board, updates)
        # Build string for updated row
        correct_line = (VB + ES + WH_SQ + BM + WH_SQ + WK + WH_SQ + BK +
                        WH_SQ + PDN4)
        generated_line = game_board.get_row(row)
        assert len(correct_line) == len(generated_line), \
            "string lengths don't match"
        assert correct_line == generated_line, \
            "generated_line doesn't match expected one"

    def test_get_odd_row(self, game_board):
        row = 7
        updates = [(24, "bm"), (26, "wk"), (27, "bk")]
        game_board = self.update_board(game_board, updates)
        # Build string for updated row
        correct_line = (WH_SQ + BM + WH_SQ + WM + WH_SQ + WK + WH_SQ + BK +
                        VB + PDN7)
        generated_line = game_board.get_row(row)
        assert len(correct_line) == len(generated_line), \
            "string lengths don't match"
        assert correct_line == generated_line, \
            "generated_line doesn't match expected one"


###################################
# #### Checkers class tests
###################################
class TestCheckersClass:
    @pytest.fixture()
    def game(self):
        return Checkers()

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
        game
    ):
        game.board.display_board("Kat", "Rob")
        captured_output = mock_stdout.getvalue()
        assert "Black: Kat" in captured_output, \
            "black player was not displayed"
        assert "White: Rob" in captured_output, \
            "white player was not displayed"

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_board_shows_board_correctly(
        self,
        mock_stdout,
        game
    ):
        game.board.display_board("Kat", "Rob")
        captured_output = mock_stdout.getvalue()
        # Build expected string that represents the starting board
        board_lines = [
            UL + (H3+NT) * 7 + H3 + UR,
            (WH_SQ+BM) * 4 + VB + PDN1 + "\n" + MID,
            VB + (BM+WH_SQ) * 4 + PDN2 + "\n" + MID,
            (WH_SQ+BM) * 4 + VB + PDN3 + "\n" + MID,
            VB + (ES+WH_SQ) * 4 + PDN4 + "\n" + MID,
            (WH_SQ+ES) * 4 + VB + PDN5 + "\n" + MID,
            VB + (WM+WH_SQ) * 4 + PDN6 + "\n" + MID,
            (WH_SQ+WM) * 4 + VB + PDN7 + "\n" + MID,
            VB + (WM+WH_SQ) * 4 + PDN8,
            LL + (H3+ST) * 7 + H3 + LR
        ]
        board = "\n".join(board_lines)
        assert board in captured_output, \
            "starting board display is incorrect"

        # Update a few pieces on the board
        updates = [(23, "bm"), (26, "wk"), (27, "bk")]
        TestBoardClass.update_board(game.board, updates)
        game.board.display_board("Kat", "Rob")
        captured_output = mock_stdout.getvalue()
        board_lines[6] = VB + (WM+WH_SQ) * 3 + BM + WH_SQ + PDN6 + "\n" + MID
        board_lines[7] = (WH_SQ+WM) * 2 + WH_SQ + WK + WH_SQ + BK + VB + \
            PDN7 + "\n" + MID
        board = "\n".join(board_lines)
        assert board in captured_output, \
            "updated board display is incorrect"
