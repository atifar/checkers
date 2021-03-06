"""Functional tests for checkers game

Following the step-by-step adventures of two imaginary actors playing
checkers against each other.

Py.test is the framework used for these tests.
"""
from io import StringIO
from unittest.mock import patch
from .checkers import Checkers


###################################
# #### Checkers game functional tests
###################################
class TestCheckersGame:

    def test_checkers_rules_and_get_player_names(self):
        # Kat and Rob have decided to challenge each other in a game of
        # checkers. They launch the checkers application, and see the game's
        # rules displayed.
        game = Checkers()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            game.show_rules()
        captured_output = mock_stdout.getvalue()
        assert "Welcome to this awesome checkers game!" in captured_output, \
            "welcome message was not displayed"
        assert "a draw which the opponent accepts." in captured_output, \
            "game rules were not displayed"

        # Then the game prompts to type in their names.
        # Kat enters hers first, then Rob does. The initial game board is
        # displayed along with the players' names. Kat has the black pieces
        # while Rob has the white ones.
        with patch('builtins.input', side_effect=['Kat', 'Rob']), \
                patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            game.get_player_names()
            game.board.display_board(game)
        captured_output = mock_stdout.getvalue()
        assert "Player for black, please type in your name: ", \
            "black player should be prompted to enter their name"
        assert "Player for white, please type in your name: ", \
            "white player should be prompted to enter their name"
        assert game.blacks_turn is True, \
            "black should be the first to move"
        assert "Kat" in captured_output, \
            "player names were not displayed"
        assert "Rob" in captured_output, \
            "player names were not displayed"

    def test_game_play_black_wins(self):
        # Kat and Rob are starting a new checkers game.
        game = Checkers()
        with patch('builtins.input', side_effect=['Kat', 'Rob', '10']), \
                patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            game.show_rules()
            game.get_player_names()
            game.get_player_move_from()
        captured_output = mock_stdout.getvalue()
        assert "Kat" in captured_output, \
            "player names were not displayed"

        # Playing with the black pieces, Kat is prompted to select a piece. She
        # selects the man on 9. (9-14).
        # Rob makes his countermove (23-18).

        # Now Kat must jump and capture Rob's man, to which she must answer by
        # capturing his man (14x23, 27x18). Now both players are down to 11
        # pieces each.

        # The continue playing through several moves. (3. 5-9, 26-23)
        # (4. 12-16, 30-26)(5. 16-19, 24x15)(6. 10x19, 23x16)(7. 11x20, 22-17)
        # (8. 7-11, 18-15)(9. 11x18, 28-24)

        # They get to the first situation where Kat takes three of Rob's pieces
        # in a triple jump. (10. 20x27, 32x5)

        # After several more moves ... (11. 8-11, 26-23)(12. 4-8, 25-22)
        # (13. 11-15, 17-13)(14. 8-11, 21-17)(15. 11-16, 23-18)
        # (16. 15-19, 17-14)(17. 19-24, 14-10)
        #
