import pickle
import copy

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board, player):
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

def is_full(board):
    return all([cell != " " for row in board for cell in row])

def save_game(state, filename='tic_tac_toe_save.pkl'):
    try:
        with open(filename, 'wb') as f:
            pickle.dump(state, f)
        print("Game saved successfully.")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game(filename='tic_tac_toe_save.pkl'):
    try:
        with open(filename, 'rb') as f:
            state = pickle.load(f)
        print("Game loaded successfully.")
        return state
    except FileNotFoundError:
        print("No saved game found.")
        return None
    except Exception as e:
        print(f"Error loading game: {e}")
        return None

def reset_board():
    return [[" " for _ in range(3)] for _ in range(3)]

def print_move_history(move_history):
    print("Game History:")
    for i, (board, player) in enumerate(move_history):
        print(f"Move {i + 1} by Player {player}:")
        print_board(board)
        print()

def print_statistics(scores, games_played, rounds_played, ties):
    print(f"Score - X: {scores.get('X', 0)}, O: {scores.get('O', 0)}")
    print(f"Games Played: {games_played}")
    print(f"Rounds Played: {rounds_played}")
    print(f"Ties: {ties}")

def print_welcome_message():
    welcome_message = r"""
 __        __   _                            _          _____ _        _____            _____
 \ \      / /__| | ___ ___  _ __ ___   ___  | |_ ___   |_   _| |__   __|_   _|__   ___  |_   _|__   ___
  \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \    | | | '_ \ / _ \| |/ _ \ / _ \   | |/ _ \ / _ \\
   \ V  V /  __/ | (_| (_) | | | | | |  __/ | || (_) |   | | | | | |  __/| | (_) |  __/   | | (_) |  __/
    \_/\_/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/    |_| |_| |_|\___||_|\___/ \___|   |_|\___/ \___|

    """
    print(welcome_message)

def print_instructions():
    instructions = """
How to Play Tic-Tac-Toe:
1. The game is played on a 3x3 grid.
2. Player 1 is X and Player 2 is O.
3. Players take turns putting their marks in empty squares.
4. The first player to get 3 of their marks in a row (up, down, across, or diagonally) is the winner.
5. When all 9 squares are full, the game is over.
6. During the game, you can enter:
   - 'r' to reset the game
   - 'u' to undo the last move
   - 's' to save the game
   - 'l' to load a saved game
   - 'rs' to reset scores
   - 'rst' to reset statistics
   - 'st' to show statistics
   - 'e' to end the game
"""
    print(instructions)

def main():
    print_welcome_message()
    print_instructions()
    state = load_game()
    if state:
        board, current_player, scores, games_played, move_history = state
        rounds_played = len(move_history)
        player1_symbol = 'X' if 'X' in scores else 'O'
        player2_symbol = 'O' if player1_symbol == 'X' else 'X'
    else:
        scores = {}
        games_played = 0
        move_history = []
        rounds_played = 0
        board = reset_board()
        current_player = None

    if not current_player:
        while True:
            player1_symbol = input("Player 1, choose your symbol (X or O): ").upper()
            if player1_symbol in ["X", "O"]:
                break
            print("Invalid choice. Please choose X or O.")
        player2_symbol = "O" if player1_symbol == "X" else "X"
        print(f"Player 1 is {player1_symbol} and Player 2 is {player2_symbol}")
        scores[player1_symbol] = 0
        scores[player2_symbol] = 0
        current_player = player1_symbol

    ties = 0

    while True:
        game_over = False

        while not game_over:
            print_board(board)
            print(f"Score - {current_player}: {scores[current_player]}, {player2_symbol if current_player == player1_symbol else player1_symbol}: {scores[player2_symbol if current_player == player1_symbol else player1_symbol]}")
            print(f"Games Played: {games_played}")
            print(f"Rounds Played: {rounds_played}")
            print(f"Ties: {ties}")
            print(f"Current Player: {current_player}")
            print(f"It's {current_player}'s turn.")
            row = input(f"Player {current_player}, enter the row (0, 1, 2), 'r' to reset, 'u' to undo, 's' to save, 'l' to load, 'rs' to reset scores, 'rst' to reset statistics, 'st' to show statistics, or 'e' to end the game: ").lower()
            if row == 'r':
                board = reset_board()
                current_player = player1_symbol
                move_history = []
                print("Game has been reset.")
                continue
            elif row == 'u':
                if move_history:
                    board, current_player = move_history.pop()
                    print("Last move undone.")
                else:
                    print("No moves to undo.")
                continue
            elif row == 's':
                save_game((board, current_player, scores, games_played, move_history))
                continue
            elif row == 'l':
                state = load_game()
                if state:
                    board, current_player, scores, games_played, move_history = state
                continue
            elif row == 'rs':
                scores = {player1_symbol: 0, player2_symbol: 0}
                print("Scores have been reset.")
                continue
            elif row == 'rst':
                scores = {player1_symbol: 0, player2_symbol: 0}
                games_played = 0
                rounds_played = 0
                ties = 0
                print("Game statistics have been reset.")
                continue
            elif row == 'st':
                print_statistics(scores, games_played, rounds_played, ties)
                continue
            elif row == 'e':
                print("Game ended by user.")
                return
            try:
                row = int(row)
                col = int(input(f"Player {current_player}, enter the column (0, 1, 2): "))
                if row not in [0, 1, 2] or col not in [0, 1, 2]:
                    raise ValueError
            except ValueError:
                print("Invalid input, please enter numbers for row and column between 0 and 2.")
                continue

            if board[row][col] != " ":
                print("Cell already taken, try again.")
                continue

            move_history.append((copy.deepcopy(board), current_player))
            board[row][col] = current_player

            print(f"Player {current_player} moved to ({row}, {col})")

            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} wins!")
                scores[current_player] += 1
                games_played += 1
                print(f"Score - {current_player}: {scores[current_player]}, {player2_symbol if current_player == player1_symbol else player1_symbol}: {scores[player2_symbol if current_player == player1_symbol else player1_symbol]}")
                game_over = True

            elif is_full(board):
                print_board(board)
                print("It's a tie!")
                games_played += 1
                ties += 1
                print(f"Score - {current_player}: {scores[current_player]}, {player2_symbol if current_player == player1_symbol else player1_symbol}: {scores[player2_symbol if current_player == player1_symbol else player1_symbol]}")
                game_over = True

            else:
                current_player = player2_symbol if current_player == player1_symbol else player1_symbol

            print(f"Current Score - {current_player}: {scores[current_player]}, {player2_symbol if current_player == player1_symbol else player1_symbol}: {scores[player2_symbol if current_player == player1_symbol else player1_symbol]}")

        print_move_history(move_history)

        if check_winner(board, current_player):
            print(f"The winner is Player {current_player}!")
        else:
            print("The game ended in a tie!")

        rounds_played += 1

        print(f"Score after round {rounds_played}: {current_player}: {scores[current_player]}, {player2_symbol if current_player == player1_symbol else player1_symbol}: {scores[player2_symbol if current_player == player1_symbol else player1_symbol]}")
        print(f"Games Played: {games_played}")
        print(f"Rounds Played: {rounds_played}")
        print(f"Ties: {ties}")

        save_game((board, current_player, scores, games_played, move_history))

        play_again = input("Do you want to play another round? (y/n): ").lower()
        if play_again != 'y':
            break

if __name__ == "__main__":
    main()