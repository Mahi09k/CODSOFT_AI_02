from django.shortcuts import render, redirect

# Game logic functions (check_win, check_draw, minimax, ai_move) should be included here

def check_win(board, player):
    """Function to check if a player has won."""
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False


def check_draw(board):
    """Function to check if the game is a draw."""
    return all([cell != ' ' for row in board for cell in row])


def minimax(board, depth, is_maximizing):
    """Minimax algorithm for AI move calculation."""
    if check_win(board, 'O'):
        return 1
    elif check_win(board, 'X'):
        return -1
    elif check_draw(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == ' ':
                    board[r][c] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[r][c] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == ' ':
                    board[r][c] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[r][c] = ' '
                    best_score = min(score, best_score)
        return best_score


def ai_move(board):
    """AI move calculation using minimax."""
    best_score = -float('inf')
    best_move = None
    for r in range(3):
        for c in range(3):
            if board[r][c] == ' ':
                board[r][c] = 'O'
                score = minimax(board, 0, False)
                board[r][c] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
    return best_move


def index(request):
    """View function for rendering the game board and handling player moves."""
    mode = request.session.get('mode', 'ai')  # Default to AI mode if mode is not set
    if request.GET.get('reset'):
        request.session['board'] = [[' ' for _ in range(3)] for _ in range(3)]
        request.session['status'] = 'Player 1\'s Turn' if mode == 'player' else 'Player\'s Turn'
        request.session['mode'] = mode
        return render(request, 'game/index.html', {
            'board': request.session['board'],
            'status': request.session['status'],
            'mode': mode
        })

    board = request.session.get('board', [[' ' for _ in range(3)] for _ in range(3)])
    status = request.session.get('status', 'Player 1\'s Turn' if mode == 'player' else 'Player\'s Turn')
    if request.GET.get('row') and request.GET.get('col'):
        row = int(request.GET.get('row'))
        col = int(request.GET.get('col'))
        if board[row][col] == ' ':
            if mode == 'player':
                current_player = 'X' if 'Player 1' in status else 'O'
                board[row][col] = current_player
                if check_win(board, current_player):
                    status = f'{current_player} Wins!'
                elif check_draw(board):
                    status = 'Draw!'
                else:
                    status = 'Player 1\'s Turn' if current_player == 'O' else 'Player 2\'s Turn'
            else:  # AI mode
                board[row][col] = 'X'
                if check_win(board, 'X'):
                    status = 'Player Wins!'
                elif check_draw(board):
                    status = 'Draw!'
                else:
                    ai_move_pos = ai_move(board)
                    if ai_move_pos:
                        board[ai_move_pos[0]][ai_move_pos[1]] = 'O'
                    if check_win(board, 'O'):
                        status = 'AI Wins!'
                    elif check_draw(board):
                        status = 'Draw!'
                    else:
                        status = 'Player\'s Turn'
    request.session['board'] = board
    request.session['status'] = status
    request.session['mode'] = mode
    return render(request, 'game/index.html', {
        'board': board,
        'status': status,
        'mode': mode
    })


def choose_mode(request):
    """View function for selecting game mode."""
    if request.method == 'POST':
        mode = request.POST.get('mode')
        if mode == 'AI':
            request.session['mode'] = 'ai'
            return redirect('ai_game_view_name')  # Redirect to AI game view
        elif mode == 'player':
            request.session['mode'] = 'player'
            return redirect('player_game_view_name')  # Redirect to player vs player game view

    return render(request, 'game/choose_mode.html')


def ai_game_view(request):
    """View function for AI vs AI or player vs AI game mode."""
    return index(request)


def player_game_view(request):
    """View function for player vs player game mode."""
    return index(request)
