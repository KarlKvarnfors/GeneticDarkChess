
class Move:

    def __init__(self, prev_game_state, from_row_col, to_row_col):
        self.prev_game_state = prev_game_state
        self.from_row_col = from_row_col
        self.to_row_col = to_row_col

    def get_possible_moves(game_state):
        moves = []
        for row in range(GameState.board_size):
            for col in range(GameState.board_size):
                piece_moves = Move.get_possible_moves_for_piece(game_state, row, col)
                if len(piece_moves) > 0:
                    moves += piece_moves
        return moves

    def get_possible_moves_for_piece(game_state, row, col):
        if game_state.board[row][col][0] != game_state.next_player:
            return []

        if game_state.board[row][col][1] == GameState.cell_piece_type_pawn:
            return Move.get_pawn_moves(game_state, row, col)
        elif game_state.board[row][col][1] == GameState.cell_piece_type_rook:
            return Move.get_rook_moves(game_state, row, col)
        elif game_state.board[row][col][1] == GameState.cell_piece_type_knight:
            return Move.get_knight_moves(game_state, row, col)
        elif game_state.board[row][col][1] == GameState.cell_piece_type_bishop:
            return Move.get_bishop_moves(game_state, row, col)
        elif game_state.board[row][col][1] == GameState.cell_piece_type_queen:
            return Move.get_queen_moves(game_state, row, col)
        elif game_state.board[row][col][1] == GameState.cell_piece_type_king:
            return Move.get_king_moves(game_state, row, col)

    def get_pawn_moves(game_state, row, col):
        moves = []

        # Initial double distance move
        if (row == 1 and
           game_state.board[row][col][0] == GameState.cell_occupation_code_black and
           game_state.board[row+1][col][0] == GameState.cell_occupation_code_empty and
           game_state.board[row+2][col][0] == GameState.cell_occupation_code_empty):
            moves.append(Move(game_state, [row, col], [row+2,col]))
        if (row == 6 and
           game_state.board[row][col][0] == GameState.cell_occupation_code_white and
           game_state.board[row-1][col][0] == GameState.cell_occupation_code_empty and
           game_state.board[row-2][col][0] == GameState.cell_occupation_code_empty):
            moves.append(Move(game_state, [row, col], [row-2,col]))

        # Regular forward move
        if (row < 7 and
           game_state.board[row][col][0] == GameState.cell_occupation_code_black and
           game_state.board[row+1][col][0] == GameState.cell_occupation_code_empty):
            moves.append(Move(game_state, [row, col], [row+1,col]))
        if (row > 0 and
           game_state.board[row][col][0] == GameState.cell_occupation_code_white and
           game_state.board[row-1][col][0] == GameState.cell_occupation_code_empty):
            moves.append(Move(game_state, [row, col], [row-1,col]))

        # Capture
        if (row < 7 and col < 7 and
           game_state.board[row][col][0] == GameState.cell_occupation_code_black and
           game_state.board[row+1][col+1][0] == GameState.cell_occupation_code_white):
            moves.append(Move(game_state, [row, col], [row+1, col+1]))
        if (row < 7 and col > 0 and
           game_state.board[row][col][0] == GameState.cell_occupation_code_black and
           game_state.board[row+1][col-1][0] == GameState.cell_occupation_code_white):
            moves.append(Move(game_state, [row, col], [row+1, col-1]))
        if (row > 0 and col < 7 and
           game_state.board[row][col][0] == GameState.cell_occupation_code_white and
           game_state.board[row-1][col+1][0] == GameState.cell_occupation_code_black):
            moves.append(Move(game_state, [row, col], [row-1, col+1]))
        if (row > 0 and col > 0 and
           game_state.board[row][col][0] == GameState.cell_occupation_code_white and
           game_state.board[row-1][col-1][0] == GameState.cell_occupation_code_black):
            moves.append(Move(game_state, [row, col], [row-1, col-1]))

        return moves

    def get_rook_moves(game_state, row, col): #excuse me for this awfully long function
        moves=[]
        if self.next_player==GameState.cell_occupation_code_black: #if black player
            for i in range(row,0,-1): #searches vertically, upwards
                if game_state.board[i][col] == GameState.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(game_state, [row, col], [i,col]))
                elif game_state.board[i][col]==GameState.cell_occupation_code_white: #capturing move
                    moves.append(Move(game_state, [row, col], [i,col]))
                elif game_state.board[i][col]==GameState.cell_occupation_code_black: #stop seaching if a black piece is found on that column
                    break
            for i in range(row,8,1): #searches vertically, downwards
                if game_state.board[i][col] == GameState.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(game_state, [row, col], [i,col]))
                elif game_state.board[i][col]==GameState.cell_occupation_code_white: #capturing move
                    moves.append(Move(game_state, [row, col], [i,col]))
                elif game_state.board[i][col]==GameState.cell_occupation_code_black: #stop seaching if a black piece is found on that column
                    break
            for i in range(col,8,1): #searches horizontally to the right of the piece
                if game_state.board[row][i] == GameState.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(game_state, [row, col], [i,col]))
                elif game_state.board[row][i]==GameState.cell_occupation_code_white: #capturing move
                    moves.append(Move(game_state, [row, col], [i,col]))
                elif game_state.board[row][i]==GameState.cell_occupation_code_black: #stop seaching if a black piece is found on that row
                    break
            for i in range(col,0,-1): #searches horizontally to the left of the piece
                if game_state.board[row][i] == GameState.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(game_state, [row, col], [i,col]))
                elif game_state.board[row][i]==GameState.cell_occupation_code_white: #capturing move
                    moves.append(Move(game_state, [row, col], [i,col]))
                elif game_state.board[row][i]==GameState.cell_occupation_code_black: #stop seaching if a black piece is found on that row
                    break


        elif self.next_player==GameState.cell_occupation_code_white: #if white player
            for i in range(row,0,-1): #searches vertically, upwards
                if game_state.board[i][col] == GameState.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(game_state, [row, col], [i,col]))
                elif game_state.board[i][col]==GameState.cell_occupation_code_black: #capturing move
                    moves.append(Move(game_state, [row, col], [i,col]))
                elif game_state.board[i][col]==GameState.cell_occupation_code_white: #stop seaching if a black piece is found on that column
                    break
            for i in range(row,8,1): #searches vertically, downwards
                if game_state.board[i][col] == GameState.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(game_state, [row, col], [i,col]))
                elif game_state.board[i][col]==GameState.cell_occupation_code_black: #capturing move
                    moves.append(Move(game_state, [row, col], [i,col]))
                elif game_state.board[i][col]==GameState.cell_occupation_code_white: #stop seaching if a black piece is found on that column
                    break
            for i in range(col,8,1): #searches horizontally to the right of the piece
                if game_state.board[row][i] == GameState.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(game_state, [row, col], [i,col]))
                elif game_state.board[row][i]==GameState.cell_occupation_code_black: #capturing move
                    moves.append(Move(game_state, [row, col], [i,col]))
                elif game_state.board[row][i]==GameState.cell_occupation_code_white: #stop seaching if a black piece is found on that row
                    break
            for i in range(col,0,-1): #searches horizontally to the left of the piece
                if game_state.board[row][i] == GameState.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(game_state, [row, col], [i,col]))
                elif game_state.board[row][i]==GameState.cell_occupation_code_black: #capturing move
                    moves.append(Move(game_state, [row, col], [i,col]))
                elif game_state.board[row][i]==GameState.cell_occupation_code_white: #stop seaching if a black piece is found on that row
                    break
        return moves

    def get_knight_moves(game_state, row, col):
        moves=[]
        possibleMoves=[[row-1,col-2],[row-2,col-1],[row-1,col+2],[row-2,col+1],[row+1,col-2],[row+2,col-1],[row+1,col+2],[row+2,col+1]]
        if self.next_player==GameState.cell_occupation_code_black: #if black player
            for move in possibleMoves:
                if (0 < move[0] < 8) and (0< move[1] < 8):
                    if game_state.board[move[0]][move[1]] == GameState.cell_occupation_code_empty: #non capturing move
                        moves.append(Move(game_state, [row, col], [move[0],move[1]]))
                    elif game_state.board[move[0]][move[1]]==GameState.cell_occupation_code_white: #capturing move
                        moves.append(Move(game_state, [row, col],[move[0],move[1]]))))

        if self.next_player==GameState.cell_occupation_code_white: #if white player
            for move in possibleMoves:
                if (0 < move[0] < 8) and (0< move[1] < 8):
                    if game_state.board[move[0]][move[1]] == GameState.cell_occupation_code_empty: #non capturing move
                        moves.append(Move(game_state, [row, col], [move[0],move[1]]))))
                    elif game_state.board[move[0]][move[1]]==GameState.cell_occupation_code_black: #capturing move
                        moves.append(Move(game_state, [row, col], [move[0],move[1]]))))
        return moves

    def get_bishop_moves(game_state, row, col):
        moves=[]
        if self.next_player==GameState.cell_occupation_code_black: #if black player
            for r,c in zip(range(row,0,-1),range(col,0,-1)): #seacrhes diag1
                if game_state.board[r][c] == GameState.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(game_state, [row, col], [r,c]))
                elif game_state.board[r][c]==GameState.cell_occupation_code_white: #capturing move
                    moves.append(Move(game_state, [row, col], [r,c]))
                elif game_state.board[r][c]==GameState.cell_occupation_code_black:
                    break
            for r,c in zip(range(row,8,1),range(col,8,1)): #seacrhes diag2
                if game_state.board[r][c] == GameState.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(game_state, [row, col], [r,c]))
                elif game_state.board[r][c]==GameState.cell_occupation_code_white: #capturing move
                    moves.append(Move(game_state, [row, col], [r,c]))
                elif game_state.board[r][c]==GameState.cell_occupation_code_black:
                    break
            for r,c in zip(range(row,8,1),range(col,0,-1)): #seacrhes diag3
                if game_state.board[r][c] == GameState.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(game_state, [row, col], [r,c]))
                elif game_state.board[r][c]==GameState.cell_occupation_code_white: #capturing move
                    moves.append(Move(game_state, [row, col], [r,c]))
                elif game_state.board[r][c]==GameState.cell_occupation_code_black:
                    break
            for r,c in zip(range(row,0,-1),range(col,8,1)): #seacrhes diag3
                if game_state.board[r][c] == GameState.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(game_state, [row, col], [r,c]))
                elif game_state.board[r][c]==GameState.cell_occupation_code_white: #capturing move
                    moves.append(Move(game_state, [row, col], [r,c]))
                elif game_state.board[r][c]==GameState.cell_occupation_code_black:
                    break
        if self.next_player==GameState.cell_occupation_code_white: #if black player
            for r,c in zip(range(row,0,-1),range(col,0,-1)): #seacrhes diag1
                if game_state.board[r][c] == GameState.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(game_state, [row, col], [r,c]))
                elif game_state.board[r][c]==GameState.cell_occupation_code_black: #capturing move
                    moves.append(Move(game_state, [row, col], [r,c]))
                elif game_state.board[r][c]==GameState.cell_occupation_code_white:
                    break
            for r,c in zip(range(row,8,1),range(col,8,1)): #seacrhes diag2
                if game_state.board[r][c] == GameState.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(game_state, [row, col], [r,c]))
                elif game_state.board[r][c]==GameState.cell_occupation_code_black: #capturing move
                    moves.append(Move(game_state, [row, col], [r,c]))
                elif game_state.board[r][c]==GameState.cell_occupation_code_white:
                    break
            for r,c in zip(range(row,8,1),range(col,0,-1)): #seacrhes diag3
                if game_state.board[r][c] == GameState.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(game_state, [row, col], [r,c]))
                elif game_state.board[r][c]==GameState.cell_occupation_code_black: #capturing move
                    moves.append(Move(game_state, [row, col], [r,c]))
                elif game_state.board[r][c]==GameState.cell_occupation_code_white:

            for r,c in zip(range(row,0,-1),range(col,8,1)): #seacrhes diag3
                if game_state.board[r][c] == GameState.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(game_state, [row, col], [r,c]))
                elif game_state.board[r][c]==GameState.cell_occupation_code_black: #capturing move
                    moves.append(Move(game_state, [row, col], [r,c]))
                elif game_state.board[r][c]==GameState.cell_occupation_code_white:
                    break

        return moves

    def get_queen_moves(game_state, row, col):
        moves = get_rook_moves(game_state, row, col)
        moves += get_bishop_moves(game_state, row, col)
        return moves

    def get_king_moves(game_state, row, col):
        return []

    def get_promoted_pawn_moves(game_state, row, col):
        return []

from GameState import GameState