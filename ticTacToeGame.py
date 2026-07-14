def display_board(board):
    print("\n")
    for i in range(3):
        print(" | ".join(board[i]))
        if i < 2:
            print("--+---+--")
    print()


def check_winner(board, player):
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True

    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(3)):
        return True

    if all(board[i][2 - i] == player for i in range(3)):
        return True

    return False


def is_board_full(board):
    for row in board:
        if " " in row:
            return False
    return True


def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        display_board(board)

        try:
            row = int(input(f"Player {current_player}, enter row (1-3): ")) - 1
            col = int(input(f"Player {current_player}, enter column (1-3): ")) - 1

            if row not in range(3) or col not in range(3):
                print("Invalid position! Please enter values between 1 and 3.")
                continue

            if board[row][col] != " ":
                print("Cell already occupied! Try again.")
                continue

            board[row][col] = current_player

            if check_winner(board, current_player):
                display_board(board)
                print(f"🎉 Player {current_player} wins!")
                break

            if is_board_full(board):
                display_board(board)
                print("🤝 It's a Tie!")
                break

            # Switch player
            current_player = "O" if current_player == "X" else "X"

        except ValueError:
            print("Please enter valid numbers.")


while True:
    play_game()

    choice = input("Do you want to play again? (yes/no): ").lower()

    if choice != "yes":
        print("Thanks for playing! 👋")
        ""
        "break"