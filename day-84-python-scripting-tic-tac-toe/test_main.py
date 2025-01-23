import pytest
from main import print_board, check_winner, is_full, save_game, load_game, reset_board, print_move_history, print_statistics

class TestTicTacToe:
    """
    Unit test class for testing the Tic-Tac-Toe game functions.
    """

    def test_board_prints_correctly(self, capsys):
        """
        Test that the board prints correctly.
        """
        board = [["X", "O", "X"], ["O", "X", "O"], ["X", "O", "X"]]
        expected_output = "X | O | X\n-----\nO | X | O\n-----\nX | O | X\n-----\n"
        print_board(board)
        captured = capsys.readouterr()
        assert expected_output in captured.out

    def test_winner_is_detected_correctly(self):
        """
        Test that the winner is detected correctly.
        """
        board = [["X", "X", "X"], ["O", " ", "O"], [" ", " ", " "]]
        assert check_winner(board, "X")
        assert not check_winner(board, "O")

    def test_board_is_full(self):
        """
        Test that the board is correctly identified as full or not full.
        """
        board = [["X", "O", "X"], ["O", "X", "O"], ["X", "O", "X"]]
        assert is_full(board)
        board = [["X", "O", "X"], ["O", " ", "O"], ["X", "O", "X"]]
        assert not is_full(board)

    def test_game_saves_and_loads_correctly(self):
        """
        Test that the game state saves and loads correctly.
        """
        state = (reset_board(), "X", {"X": 1, "O": 0}, 1, [])
        save_game(state, "test_save.pkl")
        loaded_state = load_game("test_save.pkl")
        assert state == loaded_state

    def test_board_resets_correctly(self):
        """
        Test that the board resets correctly.
        """
        board = reset_board()
        assert board == [[" " for _ in range(3)] for _ in range(3)]

    def test_move_history_prints_correctly(self, capsys):
        """
        Test that the move history prints correctly.
        """
        move_history = [([["X", " ", " "], [" ", " ", " "], [" ", " ", " "]], "X")]
        expected_output = "Move 1 by Player X:\nX |   |  \n-----\n  |   |  \n-----\n  |   |  \n-----\n"
        print_move_history(move_history)
        captured = capsys.readouterr()
        assert expected_output in captured.out

    def test_statistics_print_correctly(self, capsys):
        """
        Test that the game statistics print correctly.
        """
        scores = {"X": 1, "O": 0}
        games_played = 1
        rounds_played = 1
        ties = 0
        expected_output = "Score - X: 1, O: 0\nGames Played: 1\nRounds Played: 1\nTies: 0\n"
        print_statistics(scores, games_played, rounds_played, ties)
        captured = capsys.readouterr()
        assert expected_output in captured.out