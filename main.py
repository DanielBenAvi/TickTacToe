import PySimpleGUI as Gui

"""

"""
Gui.theme('DarkBlue2')
PLAYER = 'X'
OPPONENT = 'O'
PLAYER_FONT = 'Ariel 20'
MAIN_FONT = 'Ariel 24'
CELL_FONT = 'Stencil 60'
CELL_WIDTH = 2
CELL_HEIGHT = 1
BLANK = ''

"""
    game functions
"""


def reset_board(b):
    for row in range(len(b)):
        for col in range(len(b[row])):
            b[row][col] = BLANK
    return b


def reset_gui(w, b):
    for row in range(len(b)):
        for col in range(len(b[row])):
            w[f'-{row}{col}-'].update(BLANK, text_color='white')


def change_board(w, b):
    for row in range(len(b)):
        for col in range(len(b[row])):
            w[f'-{row}{col}-'].update(b[row][col])


def change_player(p):
    if p == 'X':
        return 'O'
    if p == 'O':
        return 'X'


def check_rows(w, b, player, opponent):
    for i in range(0, 3):
        if (b[i][0] == player and b[i][1] == player and b[i][2] == player) or \
                (b[i][0] == opponent and b[i][1] == opponent and b[i][2] == opponent):
            w[f'-{i}0-'].update(text_color='red')
            w[f'-{i}1-'].update(text_color='red')
            w[f'-{i}2-'].update(text_color='red')
            return True
    return False


def check_cols(w, b, player, opponent):
    for i in range(0, 3):
        if (b[0][i] == player and b[1][i] == player and b[2][i] == player) or \
                (b[0][i] == opponent and b[1][i] == opponent and b[2][i] == opponent):
            w[f'-0{i}-'].update(text_color='red')
            w[f'-1{i}-'].update(text_color='red')
            w[f'-2{i}-'].update(text_color='red')
            return True
    return False


def check_left_dig(w, b, player, opponent):
    if (b[0][0] == player and b[1][1] == player and b[2][2] == player) or \
            (b[0][0] == opponent and b[1][1] == opponent and b[2][2] == opponent):
        w[f'-00-'].update(text_color='red')
        w[f'-11-'].update(text_color='red')
        w[f'-22-'].update(text_color='red')
        return True
    return False


def check_right_dig(w, b, player, opponent):
    if (b[0][2] == player and b[1][1] == player and b[2][0] == player) or (
            b[0][2] == opponent and b[1][1] == opponent and b[2][0] == opponent):
        w[f'-02-'].update(text_color='red')
        w[f'-11-'].update(text_color='red')
        w[f'-20-'].update(text_color='red')
        return True
    return False


def if_game_over():
    return check_rows(window, board, PLAYER, OPPONENT) or \
           check_cols(window, board, PLAYER, OPPONENT) or \
           check_left_dig(window, board, PLAYER, OPPONENT) or \
           check_right_dig(window, board, PLAYER, OPPONENT)


def isMovesLeft(b):
    for i in range(3):
        for j in range(3):
            if b[i][j] == BLANK:
                return True
    return False


def evaluate(b):
    # Checking for Rows for X or O victory.
    for row in range(3):
        if b[row][0] == b[row][1] and b[row][1] == b[row][2]:
            if b[row][0] == PLAYER:
                return 10
            elif b[row][0] == OPPONENT:
                return -10

    # Checking for Columns for X or O victory.
    for col in range(3):
        if b[0][col] == b[1][col] and b[1][col] == b[2][col]:
            if b[0][col] == PLAYER:
                return 10
            elif b[0][col] == OPPONENT:
                return -10

    # Checking for Diagonals for X or O victory.
    if b[0][0] == b[1][1] and b[1][1] == b[2][2]:
        if b[0][0] == PLAYER:
            return 10
        elif b[0][0] == OPPONENT:
            return -10

    if b[0][2] == b[1][1] and b[1][1] == b[2][0]:
        if b[0][2] == PLAYER:
            return 10
        elif b[0][2] == OPPONENT:
            return -10

    # Else if none of them have won then return 0
    return 0


def minimax(b, depth, is_max):
    score = evaluate(b)
    # If Maximizer has won the game return his/her
    # evaluated score
    if score == 10:
        return score

    # If Minimizer has won the game return his/her
    # evaluated score
    if score == -10:
        return score

    # If there are no more moves and no winner then
    # it is a tie
    if not isMovesLeft(b):
        return 0

    # If this maximizer's move
    if is_max:
        best = -1000

        # Traverse all cells
        for i in range(3):
            for j in range(3):

                # Check if cell is empty
                if b[i][j] == BLANK:
                    # Make the move
                    b[i][j] = PLAYER
                    # Call minimax recursively and choose
                    # the maximum value
                    best = max(best, minimax(b, depth + 1, not is_max))

                    # Undo the move
                    b[i][j] = BLANK
        return best

    # If this minimizer's move
    else:
        best = 1000
        # Traverse all cells
        for i in range(3):
            for j in range(3):

                # Check if cell is empty
                if b[i][j] == BLANK:
                    # Make the move
                    b[i][j] = OPPONENT

                    # Call minimax recursively and choose
                    # the minimum value
                    best = min(best, minimax(b, depth + 1, not is_max))

                    # Undo the move
                    b[i][j] = BLANK
        return best


def findBestMove(b):
    best_val = -1000
    bm = (-1, -1)

    # Traverse all cells, evaluate minimax function for
    # all empty cells. And return the cell with optimal
    # value.
    for i in range(3):
        for j in range(3):

            # Check if cell is empty
            if b[i][j] == BLANK:

                # Make the move
                board[i][j] = PLAYER

                # compute evaluation function for this
                # move.
                move_val = minimax(board, 0, False)

                # Undo the move
                board[i][j] = BLANK

                # If the value of the current move is
                # more than the best value, then update
                # best/
                if move_val > best_val:
                    bm = (i, j)
                    best_val = move_val
    return bm


"""
    game variables
"""
game_over = False
turn = PLAYER
board = [[BLANK, BLANK, BLANK],
         [BLANK, BLANK, BLANK],
         [BLANK, BLANK, BLANK]]

layout = [[Gui.Text('Tic-Tac-Toe', expand_x=True, font=MAIN_FONT, key='-mainText-', justification='center')],
          [Gui.Button('Reset', expand_x=True, key='-reset-')],
          [Gui.Text('', auto_size_text=True, size=(CELL_WIDTH, CELL_HEIGHT), key='-00-', relief=Gui.RELIEF_SOLID,
                    border_width=2, justification='center', font='Stencil 60', enable_events=True),
           Gui.Text('', auto_size_text=True, size=(CELL_WIDTH, CELL_HEIGHT), key='-01-', relief=Gui.RELIEF_SOLID,
                    border_width=2, justification='center', font='Stencil 60', enable_events=True),
           Gui.Text('', auto_size_text=True, size=(CELL_WIDTH, CELL_HEIGHT), key='-02-', relief=Gui.RELIEF_SOLID,
                    border_width=2, justification='center', font='Stencil 60', enable_events=True)],
          [Gui.Text('', auto_size_text=True, size=(CELL_WIDTH, CELL_HEIGHT), key='-10-', relief=Gui.RELIEF_SOLID,
                    border_width=2, justification='center', font='Stencil 60', enable_events=True),
           Gui.Text('', auto_size_text=True, size=(CELL_WIDTH, CELL_HEIGHT), key='-11-', relief=Gui.RELIEF_SOLID,
                    border_width=2, justification='center', font='Stencil 60', enable_events=True),
           Gui.Text('', auto_size_text=True, size=(CELL_WIDTH, CELL_HEIGHT), key='-12-', relief=Gui.RELIEF_SOLID,
                    border_width=2, justification='center', font='Stencil 60', enable_events=True)],
          [Gui.Text('', auto_size_text=True, size=(CELL_WIDTH, CELL_HEIGHT), key='-20-', relief=Gui.RELIEF_SOLID,
                    border_width=2, justification='center', font='Stencil 60', enable_events=True),
           Gui.Text('', auto_size_text=True, size=(CELL_WIDTH, CELL_HEIGHT), key='-21-', relief=Gui.RELIEF_SOLID,
                    border_width=2, justification='center', font='Stencil 60', enable_events=True),
           Gui.Text('', auto_size_text=True, size=(CELL_WIDTH, CELL_HEIGHT), key='-22-', relief=Gui.RELIEF_SOLID,
                    border_width=2, justification='center', font='Stencil 60', enable_events=True)]]

window = Gui.Window("Tic-Tac-Toe", layout)

while True:
    event, values = window.read()
    if event == Gui.WIN_CLOSED:
        break

    if event in ['-reset-']:
        board = reset_board(board)
        reset_gui(window, board)
        game_over = False

    if event in ['-00-']:
        if board[0][0] == BLANK and not game_over:
            board[0][0] = turn
            change_board(window, board)

    if event in ['-01-']:
        if board[0][1] == BLANK and not game_over:
            board[0][1] = turn
            change_board(window, board)

    if event in ['-02-']:
        if board[0][2] == BLANK and not game_over:
            board[0][2] = turn
            change_board(window, board)

    if event in ['-10-']:
        if board[1][0] == BLANK and not game_over:
            board[1][0] = turn
            change_board(window, board)

    if event in ['-11-']:
        if board[1][1] == BLANK and not game_over:
            board[1][1] = turn
            change_board(window, board)

    if event in ['-12-']:
        if board[1][2] == BLANK and not game_over:
            board[1][2] = turn
            change_board(window, board)

    if event in ['-20-']:
        if board[2][0] == BLANK and not game_over:
            board[2][0] = turn
            change_board(window, board)

    if event in ['-21-']:
        if board[2][1] == BLANK and not game_over:
            board[2][1] = turn
            change_board(window, board)

    if event in ['-22-']:
        if board[2][2] == BLANK and not game_over:
            board[2][2] = turn
            change_board(window, board)
    """
        opponent turn
    """
    if isMovesLeft(board):
        best_move = findBestMove(board)
        board[best_move[0]][best_move[1]] = OPPONENT
        change_board(window, board)
    """
        check if game over
    """
    if if_game_over():
        game_over = True

window.close()
