from board import Board


def minimax(board, depth, alpha, beta,  maximising, color, move_log):
    opp_color = 'w' if color == 'b' else 'b'
    if depth == 0:
        return evaluate(color, board, move_log), board, move_log

    elif maximising:
        value = float('-inf')
        best_move = None
        log = move_log.copy()
        for move, square in get_all_moves(board, color, move_log):
            temp_move_log = move_log.copy()
            temp_move_log.append(square)
            evaluation = minimax(move, depth-1, alpha, beta,
                                 False, color, temp_move_log)[0]
            value = max(value, evaluation)
            if value == evaluation:
                best_move = move
                log = temp_move_log.copy()
                # print(log)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, best_move, log
    else:
        value = float('inf')
        best_move = None
        log = move_log.copy()
        for move, square in get_all_moves(board, opp_color, move_log):
            temp_move_log = move_log.copy()
            temp_move_log.append(square)
            evaluation = minimax(move, depth-1, alpha, beta,
                                 True, color, temp_move_log)[0]
            value = min(value, evaluation)
            if value == evaluation:
                best_move = move
                log = temp_move_log.copy()
        # print(log, value)
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value, best_move, log


def go_to_move(move_log, move_index):

    bord = Board(8, 8)
    bord.place_pieces()

    for move in range(move_index):
        # print(move_log[move], move)
        from_, to_ = move_log[move]
        r1, c1 = from_
        r2, c2 = to_
        moves = bord.board[r1][c1].valid_locations(bord.board)
        bord.board[r1][c1].move(bord.board, moves, r2, c2)

    return bord.board


def undo_move(move_log):
    return go_to_move(move_log, len(move_log)-1)


def find_all_pieces(color, board):
    pieces = []
    for r, row in enumerate(board):
        for c, piece in enumerate(row):
            if piece != '' and piece.color == color:
                pieces.append((piece, [r, c]))

    # print(pieces)
    return pieces


def get_all_moves(board, color, move_log):
    moves = []
    pieces = find_all_pieces(color, board)
    # print(pieces)
    for piece in pieces:
        valid_moves = piece.valid_locations(board.copy())
        for move in valid_moves:
            pos = [(piece.row, piece.col), move]
            temp_board = go_to_move(move_log, len(move_log))
            temp_board[piece.row][piece.col].move(
                temp_board, valid_moves, *move)
            moves.append((temp_board, pos))
    return moves


def find_king(color, board):
    name = color + 'K'
    for r, row in enumerate(board):
        for c, piece in enumerate(row):
            if piece == '':
                continue
            if piece.name == name:
                return (r, c)


def find_all_pieces(color, board):
    pieces = []
    for row in board:
        for piece in row:
            if piece != '' and piece.color == color:
                pieces.append(piece)
    return pieces


def find_material_point(color, board):
    points = 0
    pieces = find_all_pieces(color, board)
    for piece in pieces:
        points += Board.piece_points[piece.name[1]]
    return points


def evaluate_material(color, board):
    opp_color = 'w' if color == 'b' else 'b'
    material_difference = (find_material_point(
        color, board) - find_material_point(opp_color, board))*5
    return material_difference


def evaluate_space_control(color, board):
    score = 0
    pieces = find_all_pieces(color, board)
    moves = []
    for piece in pieces:
        moves.extend(piece.valid_locations(board))
    score += len(moves)

    if (3, 3) in moves:
        score += (moves.count((3, 3)) * 5)
    if (3, 4) in moves:
        score += (moves.count((3, 3)) * 5)
    if (4, 3) in moves:
        score += (moves.count((3, 3)) * 5)
    if (4, 4) in moves:
        score += (moves.count((3, 3)) * 5)

    return score


def evaluate_king_safety(color, board, move_log):
    opp_color = 'w' if color == 'b' else 'b'
    score = 0
    row, col = find_king(color, board)
    all_moves = [(row, col-1),
                 (row, col+1),
                 (row-1, col),
                 (row+1, col),
                 (row+1, col+1),
                 (row-1, col-1),
                 (row+1, col-1),
                 (row-1, col+1)]
    for r, c in all_moves:
        if r not in range(len(board)) or c not in range(len(board[0])):
            continue
        if board[r][c] == '':
            score -= 2
        elif board[r][c].color != color:
            score -= 7
        elif board[r][c].color == color:
            score += 5

    if check_for_checkmate(board, color, move_log):
        score -= 100000
    if check_for_check(board, color):
        score -= 100000

    if check_for_checkmate(board, opp_color, move_log):
        score += 100000
    if check_for_check(board, opp_color):
        score += 10

    return score


def evaluate(color, board, move_log):
    material = evaluate_material(color, board)
    space = evaluate_space_control(color, board)
    king_safety = evaluate_king_safety(color, board, move_log)

    return material + space + king_safety


def find_king(color, board):
    name = color + 'K'
    for r, row in enumerate(board):
        for c, piece in enumerate(row):
            if piece == '':
                continue
            if piece.name == name:
                return (r, c)


def check_for_check(board, turn):
    valid_locations = []
    king_pos = find_king(turn, board)
    for r, row in enumerate(board):
        for c, piece in enumerate(row):
            if piece != '' and piece.color != turn:
                valid_locations.extend(piece.valid_locations(board))
    if king_pos in valid_locations:
        return True
    else:
        return False


def check_for_checkmate(board, turn, move_log):
    mate = Board(8, 8)
    mate.place_pieces()
    for from_, to_ in move_log:
        r1, c1 = from_
        r2, c2 = to_
        moves = mate.board[r1][c1].valid_locations(mate.board)
        mate.board[r1][c1].move(mate.board, moves, r2, c2)

    for r, row in enumerate(board):
        for c, piece in enumerate(row):
            if piece != '' and piece.color == turn:
                for r2, c2 in piece.valid_locations(board):
                    mate.board[r][c].move(
                        mate.board, piece.valid_locations(board), r2, c2)
                    if not check_for_check(mate.board, turn):
                        return False

                    else:
                        mate.board = go_to_move(move_log, len(move_log))
    return True
