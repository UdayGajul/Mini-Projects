# Tic Tac Toe Game
from random import choice


def print_board(b):
    for i in range(0, 9, 3):
        print(f"{b[i]} | {b[i+1]} | {b[i+2]}")
        if i < 6:
            print("--+---+--")
    print()


def check_win(b, p):
    wins = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]
    return any(all(b[i] == p for i in combo) for combo in wins)


def check_draw(b):
    return all(isinstance(x, str) for x in b)


def get_move(b):
    while True:
        try:
            m = int(input("Choose position (1-9): ")) - 1
            if 0 <= m < 9 and isinstance(b[m], int):
                return m
        except:
            pass


def play(vs_computer=True):
    board = list(range(1, 10))
    user = input("Choose X or O: ").upper()
    comp = "O" if user == "X" else "X"
    turn = "X"

    while True:
        print_board(board)

        if turn == user:
            move = get_move(board)
        else:
            print("Computer move...\n")
            move = choice([i for i, x in enumerate(board) if isinstance(x, int)])

        board[move] = turn

        if check_win(board, turn):
            print_board(board)
            print(f"{'You' if turn==user else 'Computer'} win!")
            break
        if check_draw(board):
            print_board(board)
            print("Draw!")
            break

        turn = "O" if turn == "X" else "X"


def play_friend():
    board = list(range(1, 10))
    turn = "X"

    while True:
        print_board(board)
        print(f"Player {turn}'s turn")

        move = get_move(board)
        board[move] = turn

        if check_win(board, turn):
            print_board(board)
            print(f"Player {turn} wins!")
            break
        if check_draw(board):
            print_board(board)
            print("Draw!")
            break

        turn = "O" if turn == "X" else "X"


# main
try:
    mode = int(input("Welcom to Tic Tac Toe 🎮\nPlay with 1. Computer or  2. Friend: "))
    if mode == 1:
        play(True)
    elif mode == 2:
        play_friend()
except:
    print("Invalid input")
