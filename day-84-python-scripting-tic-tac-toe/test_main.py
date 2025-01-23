import unittest
from main import print_board, check_winner, is_full, save_game, load_game, reset_board, print_move_history, print_statistics

class TestTicTacToe(unittest.TestCase):

    def board_prints_correctly(self):
        board = [["X", "O", "X"], ["O", "X", "O"], ["X", "O", "X"]]
        expected_output = "X | O | X\n-----\nO | X | O\n-----\nX | O | X\n-----\n"
        with self.assertLogs() as log:
            print_board(board)
        self.assertIn(expected_output, log.output[0])

    def winner_is_detected_correctly(self):
        board = [["X", "X", "X"], ["O", " ", "O"], [" ", " ", " "]]
        self.assertTrue(check_winner(board, "X"))
        self.assertFalse(check_winner(board, "O"))

    def board_is_full(self):
        board = [["X", "O", "X"], ["O", "X", "O"], ["X", "O", "X"]]
        self.assertTrue(is_full(board))
        board = [["X", "O", "X"], ["O", " ", "O"], ["X", "O", "X"]]
        self.assertFalse(is_full(board))

    def game_saves_and_loads_correctly(self):
        state = (reset_board(), "X", {"X": 1, "O": 0}, 1, [])
        save_game(state, "test_save.pkl")
        loaded_state = load_game("test_save.pkl")
        self.assertEqual(state, loaded_state)

    def board_resets_correctly(self):
        board = reset_board()
        self.assertEqual(board, [[" " for _ in range(3)] for _ in range(3)])

    def move_history_prints_correctly(self):
        move_history = [([["X", " ", " "], [" ", " ", " "], [" ", " ", " "]], "X")]
        expected_output = "Move 1 by Player X:\nX |   |  \n-----\n  |   |  \n-----\n  |   |  \n-----\n"
        with self.assertLogs() as log:
            print_move_history(move_history)
        self.assertIn(expected_output, log.output[0])

    def statistics_print_correctly(self):
        scores = {"X": 1, "O": 0}
        games_played = 1
        rounds_played = 1
        ties = 0
        expected_output = "Score - X: 1, O: 0\nGames Played: 1\nRounds Played: 1\nTies: 0\n"
        with self.assertLogs() as log:
            print_statistics(scores, games_played, rounds_played, ties)
        self.assertIn(expected_output, log.output[0])

if __name__ == "__main__":
    unittest.main()