"""Unit tests for checkers game"""

from copy import copy
from io import StringIO
from unittest.mock import patch
import pytest
from .checkers import Checkers, Board
from .checkers import PIECES


###################################
# #### Board class tests
###################################
def update_board(board, updates):
    """Return copy of board with updated squares"""
    board_copy = copy(board)
    for index, value in updates:
        board_copy.squares[index] = value
    return board_copy


def test_get_square_returns_stored_value():
    game_board = Board()
    game_board.squares[5] = "Doodly doo"
    assert game_board.get_square(5) == "Doodly doo"


def test_get_square_invalid_index():
    game_board = Board()
    pytest.raises(IndexError, game_board.get_square, 32)


def test_board_initial_piece_locations():
    game_board = Board()
    for index in range(12):
        assert game_board.get_square(index) == PIECES["black man"]
    for index in range(12, 20):
        assert game_board.get_square(index) == ""
    for index in range(20, 32):
        assert game_board.get_square(index) == PIECES["white man"]


def test_get_board_stats():
    updates = [(8, ""), (10, ""), (16, "wk"), (20, ""), (22, "")]
    game_board = Board()
    game_board = update_board(game_board, updates)
    stats = game_board.get_board_stats()
    assert stats["wk"] == 1, "incorrect number of white kings"
    assert stats["wm"] == 10, "incorrect number of white men"
    assert stats["bk"] == 0, "incorrect number of black kings"
    assert stats["bm"] == 10, "incorrect number of black men"
    assert stats[""] == 11, "incorrect number of empty squares"


###################################
# #### Checkers class tests
###################################
@patch('builtins.input', side_effect=['Kat', 'Rob'])
def test_game_updates_default_player_names(mock_input):
    game = Checkers()
    assert game.black_name == "Peter"
    assert game.white_name == "Amanda"
    game.play_game()
    assert game.black_name == "Kat"
    assert game.white_name == "Rob"


@patch('builtins.input', side_effect=['Kat', 'Rob'])
@patch('sys.stdout', new_callable=StringIO)
def test_board_display_shows_names_with_sides(mock_stdout, mock_input):
    game = Checkers()
    game.play_game()
    captured_output = mock_stdout.getvalue()
    assert "Kat plays with the black pieces." in captured_output, \
        "black player was not displayed"
    assert "Rob plays with the white pieces." in captured_output, \
        "white player was not displayed"


@patch('builtins.input', side_effect=['Kat', 'Rob'])
def test_game_creates_initial_board(mock_input):
    game = Checkers()
    assert game.board, "game did't create the board"
