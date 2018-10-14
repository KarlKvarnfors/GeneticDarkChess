from GameState import Move, GameState
import math
import numpy


# Captured pieces heuristic

def captured_pieces_heuristic(game_state):
    relative_values = [1, 5, 3, 3, 9, 1000, 9]
    value = 0
    if other_player(game_state.next_player) == game_state.cell_occupation_code_white:
        for piece in game_state.captured_black_pieces:
            value += relative_values[piece]

    if other_player(game_state.next_player) == GameState.cell_occupation_code_black:
        for piece in game_state.captured_white_pieces:
            value += relative_values[piece]

    normalizing_factor = 9 * 9 + 4 * 3 + 5 * 2 + 1000
    value = 2 * value / normalizing_factor - 1
    return value


# Protected King Heuristic, checks for protected king

def protected_king_heuristic(game_state):
    # For rows and diagonals
        # If closest piece is own piece or border, continue
        # If closest piece is enemy piece or unknown, break
            # Return -1
    # Return 1
    king_row = None
    king_col = None
    player = game_state.next_player
    
    for row in range(game_state.board_size):
        for col in range(game_state.board_size):
            if (game_state.board[row][col][0] == player and game_state.board[row][col][1] == game_state.cell_piece_type_king):
                king_row, king_col = row, col
                    
    for row in range(king_row + 1, game_state.board_size):
        current_cell_occupation_code = game_state.board[row][king_col][0]
        
        if current_cell_occupation_code == player:
            break
        elif current_cell_occupation_code == game_state.cell_occupation_code_empty:
            continue
        elif current_cell_occupation_code == game_state.cell_occupation_code_fog:
            return -1
        else:
            return -1
    
    for row in range(king_row - 1, -1, -1):
        current_cell_occupation_code = game_state.board[row][king_col][0]
        
        if current_cell_occupation_code == player:
            break
        elif current_cell_occupation_code == game_state.cell_occupation_code_empty:
            continue
        elif current_cell_occupation_code == game_state.cell_occupation_code_fog:
            return -1
        else:
            return -1
        
    for col in range(king_col + 1, game_state.board_size):
        current_cell_occupation_code = game_state.board[king_row][col][0]
        
        if current_cell_occupation_code == player:
            break
        elif current_cell_occupation_code == game_state.cell_occupation_code_empty:
            continue
        elif current_cell_occupation_code == game_state.cell_occupation_code_fog:
            return -1
        else:
            return -1
        
    for col in range(king_col - 1, -1, -1):
        current_cell_occupation_code = game_state.board[king_row][col][0]
        
        if current_cell_occupation_code == player:
            break
        elif current_cell_occupation_code == game_state.cell_occupation_code_empty:
            continue
        elif current_cell_occupation_code == game_state.cell_occupation_code_fog:
            return -1
        else:
            return -1
    
    i = 1
    while king_row + i < game_state.board_size and king_col + i < game_state.board_size:
        current_cell_occupation_code = game_state.board[king_row + i][king_col + i][0]
        
        if current_cell_occupation_code == player:
            break
        elif current_cell_occupation_code == game_state.cell_occupation_code_empty:
            continue
        elif current_cell_occupation_code == game_state.cell_occupation_code_fog:
            return -1
        else:
            return -1
        i += 1
        
    i = 1
    while king_row - i > -1 and king_col + i < game_state.board_size:
        current_cell_occupation_code = game_state.board[king_row - i][king_col + i][0]
        
        if current_cell_occupation_code == player:
            break
        elif current_cell_occupation_code == game_state.cell_occupation_code_empty:
            continue
        elif current_cell_occupation_code == game_state.cell_occupation_code_fog:
            return -1
        else:
            return -1
        i += 1
        
    i = 1
    while king_row + i < game_state.board_size and king_col - i > -1:
        current_cell_occupation_code = game_state.board[king_row + i][king_col - i][0]
        
        if current_cell_occupation_code == player:
            break
        elif current_cell_occupation_code == game_state.cell_occupation_code_empty:
            continue
        elif current_cell_occupation_code == game_state.cell_occupation_code_fog:
            return -1
        else:
            return -1
        i += 1
        
    i = 1
    while king_row - i > -1 and king_col - i > -1:
        current_cell_occupation_code = game_state.board[king_row - i][king_col - i][0]
        
        if current_cell_occupation_code == player:
            break
        elif current_cell_occupation_code == game_state.cell_occupation_code_empty:
            continue
        elif current_cell_occupation_code == game_state.cell_occupation_code_fog:
            return -1
        else:
            return -1
        i += 1
        
    return 1
    
    
# Protected Play Heuristic, checks for protected pieces

def protected_play_heuristic(game_state):
    relative_values = [1, 5, 3, 3, 9, 0, 9]
    value = 0
    moves = get_possible_moves_func(game_state)
    normalizing_factor = 0
    for move in moves:
        if (game_state.board[move.from_row_col[0]][move.from_row_col[1]][0] == other_player(game_state.next_player) and
            game_state.board[move.to_row_col[0]][move.to_row_col[1]][0] == other_player(game_state.next_player)):
            piece = game_state.board[move.from_row_col[0]][move.from_row_col[1]][1]
            value += relative_values[piece]
            normalizing_factor += max(relative_values)
    if normalizing_factor != 0:
        value = 2 * value / normalizing_factor - 1
    return value
    # For pieces
        # If protected, += relative value of piece
    # Normalize, return
    

# Information Heuristic, checks for number of visible pieces

def information_heuristic(game_state):
    # For squares
        # If visible
            # Visible squares += 1
    # Normalize, return
    
    visible_cells = 0
    for row in range(game_state.board_size):
            for col in range(game_state.board_size):
                if game_state.board[row][col][0] != game_state.cell_occupation_code_fog:
                    visible_cells += 1
    value = visible_cells / 32 - 1
    return value


# Threatened Pieces Heuristic (Aggressive), checks for number of threatened enemy pieces

def agg_threatened_pieces_heuristic(game_state):
    relative_values = [1, 5, 3, 3, 9, 20, 9]
    value = 0
    moves = get_possible_moves_func(game_state)
    normalizing_factor = 0
    for move in moves:
        if (game_state.board[move.from_row_col[0]][move.from_row_col[1]][0] == other_player(game_state.next_player) and
            game_state.board[move.to_row_col[0]][move.to_row_col[1]][0] == game_state.next_player):
            piece = game_state.board[move.from_row_col[0]][move.from_row_col[1]][1]
            value += relative_values[piece]
            normalizing_factor += max(relative_values)
    if normalizing_factor != 0:
        value = 2 * value / normalizing_factor - 1
    return value
    # For own pieces
        # Get next moves
        # For moves
            # If move threatens enemy piece
                # Threatened pieces += 1
                # (Threatened value += relative value of threatened piece)
    # Normalize, return


# Threatened Pieces Heuristic (Defensive), checks for  number of threatened own pieces

def def_threatened_pieces_heuristic(game_state):
    relative_values = [1, 5, 3, 3, 9, 1000, 9]
    value = 0
    moves = get_possible_moves_func(game_state)
    normalizing_factor = 0
    for move in moves:
        if (game_state.board[move.from_row_col[0]][move.from_row_col[1]][0] == game_state.next_player and
            game_state.board[move.to_row_col[0]][move.to_row_col[1]][0] == other_player(game_state.next_player)):
            
            piece = game_state.board[move.from_row_col[0]][move.from_row_col[1]][1]
            value -= relative_values[piece]
            normalizing_factor += max(relative_values)
    if normalizing_factor != 0:
        value = 2 * value / normalizing_factor - 1
    return value
    # For visible enemy pieces
        # Get next moves
        # For moves
            # If move threatens own piece
            # Threatened pieces += 1
            # (Threatened value += relative value of threatened piece)
    # Normalize, return

    
# TODO : insert definition of heuristics here

# The same heuristics are going to be used by each player,
# it's therefore a constant
HEURISTICS = [
    captured_pieces_heuristic,
    protected_play_heuristic,
    information_heuristic,
    agg_threatened_pieces_heuristic,
    def_threatened_pieces_heuristic
]





def other_player(player):
    if player == 1:
        return 2
    if player == 2:
        return 1

    
def get_possible_moves_func(game_state):
    moves = []
    for row in range(game_state.board_size):
        for col in range(game_state.board_size):
            piece_moves = get_possible_moves_for_piece_func(game_state, row, col)
            if len(piece_moves) > 0:
                moves += piece_moves
    return moves

def get_possible_moves_for_piece_func(game_state, row, col):
    if game_state.board[row][col][0] == game_state.cell_occupation_code_empty or game_state.board[row][col][0] == game_state.cell_occupation_code_fog:
        return []

    if game_state.board[row][col][1] == game_state.cell_piece_type_pawn:
        return get_pawn_moves_func(game_state, row, col)
    elif game_state.board[row][col][1] == game_state.cell_piece_type_rook:
        return get_rook_moves_func(game_state, row, col)
    elif game_state.board[row][col][1] == game_state.cell_piece_type_knight:
        return get_knight_moves_func(game_state, row, col)
    elif game_state.board[row][col][1] == game_state.cell_piece_type_bishop:
        return get_bishop_moves_func(game_state, row, col)
    elif game_state.board[row][col][1] == game_state.cell_piece_type_queen:
        return get_queen_moves_func(game_state, row, col)
    elif game_state.board[row][col][1] == game_state.cell_piece_type_king:
        return get_king_moves_func(game_state, row, col)
    elif game_state.board[row][col][1] == game_state.cell_piece_type_promoted_pawn:
        return get_promoted_pawn_moves_func(game_state, row, col)

def get_pawn_moves_func(game_state, row, col):
    moves = []

    # Capture
    if (row < 7 and col < 7 and
       game_state.board[row][col][0] == game_state.cell_occupation_code_black and
       game_state.board[row+1][col+1][0] == game_state.cell_occupation_code_white):
        moves.append(Move(game_state, [row, col], [row+1, col+1]))
    if (row < 7 and col < 7 and
       game_state.board[row][col][0] == game_state.cell_occupation_code_black and
       game_state.board[row+1][col+1][0] == game_state.cell_occupation_code_black):
        moves.append(Move(game_state, [row, col], [row+1, col+1]))
    if (row < 7 and col > 0 and
       game_state.board[row][col][0] == game_state.cell_occupation_code_black and
       game_state.board[row+1][col-1][0] == game_state.cell_occupation_code_white):
        moves.append(Move(game_state, [row, col], [row+1, col-1]))
    if (row < 7 and col > 0 and
       game_state.board[row][col][0] == game_state.cell_occupation_code_black and
       game_state.board[row+1][col-1][0] == game_state.cell_occupation_code_black):
        moves.append(Move(game_state, [row, col], [row+1, col-1]))
    if (row > 0 and col < 7 and
       game_state.board[row][col][0] == game_state.cell_occupation_code_white and
       game_state.board[row-1][col+1][0] == game_state.cell_occupation_code_black):
        moves.append(Move(game_state, [row, col], [row-1, col+1]))
    if (row > 0 and col < 7 and
       game_state.board[row][col][0] == game_state.cell_occupation_code_white and
       game_state.board[row-1][col+1][0] == game_state.cell_occupation_code_white):
        moves.append(Move(game_state, [row, col], [row-1, col+1]))
    if (row > 0 and col > 0 and
       game_state.board[row][col][0] == game_state.cell_occupation_code_white and
       game_state.board[row-1][col-1][0] == game_state.cell_occupation_code_black):
        moves.append(Move(game_state, [row, col], [row-1, col-1]))
    if (row > 0 and col > 0 and
       game_state.board[row][col][0] == game_state.cell_occupation_code_white and
       game_state.board[row-1][col-1][0] == game_state.cell_occupation_code_white):
        moves.append(Move(game_state, [row, col], [row-1, col-1]))

    return moves

def get_rook_moves_func(game_state, row, col): #excuse me for this awfully long function
    moves=[]
    if game_state.board[row][col][0] == game_state.cell_occupation_code_black: #if black player
        for i in range(row-1,-1,-1): #searches vertically, upwards
            if game_state.board[i][col][0] == game_state.cell_occupation_code_white: #capturing move
                moves.append(Move(game_state, [row, col], [i, col]))
                break
            elif game_state.board[i][col][0] == game_state.cell_occupation_code_black: #guarding move
                moves.append(Move(game_state, [row, col], [i, col]))
                break
        for i in range(row+1,8,1): #searches vertically, downwards
            if game_state.board[i][col][0] == game_state.cell_occupation_code_white: #capturing move
                moves.append(Move(game_state, [row, col], [i, col]))
                break
            elif game_state.board[i][col][0] == game_state.cell_occupation_code_black: #guarding move
                moves.append(Move(game_state, [row, col], [i, col]))
                break
        for i in range(col+1,8,1): #searches horizontally to the right of the piece
            if game_state.board[row][i][0] == game_state.cell_occupation_code_white: #capturing move
                moves.append(Move(game_state, [row, col], [row, i]))
                break
            elif game_state.board[row][i][0] == game_state.cell_occupation_code_black: #guarding move
                moves.append(Move(game_state, [row, col], [row, i]))
                break
        for i in range(col-1,-1,-1): #searches horizontally to the left of the piece
            if game_state.board[row][i][0] == game_state.cell_occupation_code_white: #capturing move
                moves.append(Move(game_state, [row, col], [row, i]))
                break
            elif game_state.board[row][i][0] == game_state.cell_occupation_code_black: #guarding move
                moves.append(Move(game_state, [row, col], [row, i]))
                break
    elif game_state.board[row][col][0] == game_state.cell_occupation_code_white: #if white player
        for i in range(row-1,-1,-1): #searches vertically, upwards
            if game_state.board[i][col][0] == game_state.cell_occupation_code_black: #capturing move
                moves.append(Move(game_state, [row, col], [i, col]))
                break
            elif game_state.board[i][col][0] == game_state.cell_occupation_code_white: #guarding move
                moves.append(Move(game_state, [row, col], [i, col]))
                break
        for i in range(row+1,8,1): #searches vertically, downwards
            if game_state.board[i][col][0] == game_state.cell_occupation_code_black: #capturing move
                moves.append(Move(game_state, [row, col], [i, col]))
                break
            elif game_state.board[i][col][0] == game_state.cell_occupation_code_white: #guarding move
                moves.append(Move(game_state, [row, col], [i, col]))
                break
        for i in range(col+1,8,1): #searches horizontally to the right of the piece
            if game_state.board[row][i][0] == game_state.cell_occupation_code_black: #capturing move
                moves.append(Move(game_state, [row, col], [row, i]))
                break
            elif game_state.board[row][i][0] == game_state.cell_occupation_code_white: #guarding move
                moves.append(Move(game_state, [row, col], [row, i]))
                break
        for i in range(col-1,-1,-1): #searches horizontally to the left of the piece
            if game_state.board[row][i][0] == game_state.cell_occupation_code_black: #capturing move
                moves.append(Move(game_state, [row, col], [row, i]))
                break
            elif game_state.board[row][i][0] == game_state.cell_occupation_code_white: #guarding move
                moves.append(Move(game_state, [row, col], [row, i]))
                break
    return moves

def get_knight_moves_func(game_state, row, col):
    moves=[]
    possibleMoves=[[row-1,col-2],[row-2,col-1],[row-1,col+2],[row-2,col+1],[row+1,col-2],[row+2,col-1],[row+1,col+2],[row+2,col+1]]
    if game_state.board[row][col][0] == game_state.cell_occupation_code_black: #if black player
        for move in possibleMoves:
            if (0 <= move[0] < 8) and (0 <= move[1] < 8):
                if game_state.board[move[0]][move[1]][0] == game_state.cell_occupation_code_black: #guarding move
                    moves.append(Move(game_state, [row, col], [move[0],move[1]]))
                elif game_state.board[move[0]][move[1]][0] == game_state.cell_occupation_code_white: #capturing move
                    moves.append(Move(game_state, [row, col],[move[0],move[1]]))

    if game_state.board[row][col][0] == game_state.cell_occupation_code_white: #if white player
        for move in possibleMoves:
            if (0 <= move[0] < 8) and (0 <= move[1] < 8):
                if game_state.board[move[0]][move[1]][0] == game_state.cell_occupation_code_white: #guarding move
                    moves.append(Move(game_state, [row, col], [move[0],move[1]]))
                elif game_state.board[move[0]][move[1]][0] == game_state.cell_occupation_code_black: #capturing move
                    moves.append(Move(game_state, [row, col], [move[0],move[1]]))
    return moves

def get_bishop_moves_func(game_state, row, col):
    moves=[]
    if game_state.board[row][col][0] == game_state.cell_occupation_code_black: #if black player
        for r,c in zip(range(row-1,-1,-1),range(col-1,-1,-1)): #seacrhes diag1
            if game_state.board[r][c][0] == game_state.cell_occupation_code_white: #capturing move
                moves.append(Move(game_state, [row, col], [r,c]))
                break
            elif game_state.board[r][c][0] == game_state.cell_occupation_code_black: #guarding move
                moves.append(Move(game_state, [row, col], [r,c]))
                break
        for r,c in zip(range(row+1,8,1),range(col+1,8,1)): #seacrhes diag2
            if game_state.board[r][c][0] == game_state.cell_occupation_code_white: #capturing move
                moves.append(Move(game_state, [row, col], [r,c]))
                break
            elif game_state.board[r][c][0] == game_state.cell_occupation_code_black: #guarding move
                moves.append(Move(game_state, [row, col], [r,c]))
                break
        for r,c in zip(range(row+1,8,1),range(col-1,-1,-1)): #seacrhes diag3
            if game_state.board[r][c][0] == game_state.cell_occupation_code_white: #capturing move
                moves.append(Move(game_state, [row, col], [r,c]))
                break
            elif game_state.board[r][c][0] == game_state.cell_occupation_code_black: #guarding move
                moves.append(Move(game_state, [row, col], [r,c]))
                break
        for r,c in zip(range(row-1,-1,-1),range(col+1,8,1)): #seacrhes diag3
            if game_state.board[r][c][0] == game_state.cell_occupation_code_white: #capturing move
                moves.append(Move(game_state, [row, col], [r,c]))
                break
            elif game_state.board[r][c][0] == game_state.cell_occupation_code_black: #guarding move
                moves.append(Move(game_state, [row, col], [r,c]))
                break
    if game_state.board[row][col][0] == game_state.cell_occupation_code_white: #if white player
        for r,c in zip(range(row-1,-1,-1),range(col-1,-1,-1)): #seacrhes diag1
            if game_state.board[r][c][0] == game_state.cell_occupation_code_black: #capturing move
                moves.append(Move(game_state, [row, col], [r,c]))
                break
            elif game_state.board[r][c][0] == game_state.cell_occupation_code_white: #guarding move
                moves.append(Move(game_state, [row, col], [r,c]))
                break
        for r,c in zip(range(row+1,8,1),range(col+1,8,1)): #seacrhes diag2
            if game_state.board[r][c][0] == game_state.cell_occupation_code_black: #capturing move
                moves.append(Move(game_state, [row, col], [r,c]))
                break
            elif game_state.board[r][c][0] == game_state.cell_occupation_code_white: #guarding move
                moves.append(Move(game_state, [row, col], [r,c]))
                break
        for r,c in zip(range(row+1,8,1),range(col-1,-1,-1)): #seacrhes diag3
            if game_state.board[r][c][0] == game_state.cell_occupation_code_black: #capturing move
                moves.append(Move(game_state, [row, col], [r,c]))
                break
            elif game_state.board[r][c][0] == game_state.cell_occupation_code_white: #guarding move
                moves.append(Move(game_state, [row, col], [r,c]))
                break
        for r,c in zip(range(row-1,-1,-1),range(col+1,8,1)): #seacrhes diag3
            if game_state.board[r][c][0] == game_state.cell_occupation_code_black: #capturing move
                moves.append(Move(game_state, [row, col], [r,c]))
                break
            elif game_state.board[r][c][0] == game_state.cell_occupation_code_white: #guarding move
                moves.append(Move(game_state, [row, col], [r,c]))
                break

    return moves

def get_queen_moves_func(game_state, row, col):
    moves = get_rook_moves_func(game_state, row, col)
    moves += get_bishop_moves_func(game_state, row, col)
    return moves

def get_king_moves_func(game_state, row, col):
    moves=[]
    possibleMoves=[(row-1,col-1),(row-1,col),(row-1,col+1),(row,col-1),(row,col+1),(row+1,col-1),(row+1,col),(row+1,col+1)]
    if game_state.board[row][col][0]==game_state.cell_occupation_code_black: #if black player
        for move in possibleMoves:
            if (0 <= move[0] < 8) and (0 <= move[1] < 8):
                if game_state.board[move[0]][move[1]][0] == game_state.cell_occupation_code_black: #guarding move
                    moves.append(Move(game_state, [row, col], [move[0],move[1]]))
                elif game_state.board[move[0]][move[1]][0] == game_state.cell_occupation_code_white: #capturing move
                    moves.append(Move(game_state, [row, col],[move[0],move[1]]))

    if game_state.board[row][col][0]==game_state.cell_occupation_code_white: #if white player
        for move in possibleMoves:
            if (0 <= move[0] < 8) and (0 <= move[1] < 8):
                if game_state.board[move[0]][move[1]][0] == game_state.cell_occupation_code_white: #guarding move
                    moves.append(Move(game_state, [row, col], [move[0],move[1]]))
                elif game_state.board[move[0]][move[1]][0] == game_state.cell_occupation_code_black: #capturing move
                    moves.append(Move(game_state, [row, col], [move[0],move[1]]))
    return moves

def get_promoted_pawn_moves_func(game_state, row, col):
    return get_queen_moves_func(game_state, row, col)

def heuristic_A(game_state):
    other_player = GameState.cell_occupation_code_empty
    if game_state.next_player == GameState.cell_occupation_code_white:
        other_player = GameState.cell_occupation_code_black
    elif game_state.next_player == GameState.cell_occupation_code_black:
        other_player = GameState.cell_occupation_code_white

    return player_heuristic(game_state, game_state.next_player) - player_heuristic(game_state, other_player)



def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

# returns the k-th bernstein polynomial in base n
def bernstein(k, n):
    return lambda x : nCr(n,k) * (x**k) * ( (1-x)**(n-k) )

def get_progress(game_state):
    # TODO : calculate according to captured units, and not units present
    #        on the board (cannot see all the ennemy pieces)
    number_of_pieces = 0
    for row in range(game_state.board_size):
        for col in range(game_state.board_size):
            if (game_state.board[row][col][0] == GameState.cell_occupation_code_black or
                game_state.board[row][col][0] == GameState.cell_occupation_code_white ):
                number_of_pieces += 1
    return number_of_pieces/64

def h(game_state, weights):
    """ returns the heuristic combining all those from HEURISTICS according to the right weights"""
    n = weights.shape[1]-1 # the bernstein basis order
    B = lambda _x : numpy.array([ [bernstein(_k,n)(_x)] for _k in range(n+1) ])
    H = lambda _game_state : numpy.array([
        _heuristic(_game_state) for _heuristic in HEURISTICS
    ])
    # print "H : ", H(game_state)
    # print "w : ", weights
    x = get_progress(game_state)
    # print "progress : ", x
    ret = numpy.dot( H(game_state) , numpy.dot(weights,B(x)) )
    # print "h(x,w) : ", ret[0]
    # H(game_state).transpose * W * B(x) :
    return ret[0]

def bernsteinweight_per_heuristic(nr_of_pieces, basis, degree):
    t=nr_of_pieces/32
    #assuming the bernstein basis is 3:
    b=basis
    d=degree
    bernsteinweight = bernstein(b, d)
    return bernsteinweight(t)


# temporary function
def heuristic_weights_shape():
    return [len(HEURISTICS), 3]
