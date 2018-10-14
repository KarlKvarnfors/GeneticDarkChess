class Move:
    def __init__(self, prev_game_state, from_row_col, to_row_col):
        self.prev_game_state = prev_game_state
        self.from_row_col = from_row_col
        self.to_row_col = to_row_col

class GameState:

    board_size = 8

    cell_occupation_code_empty = 0
    cell_occupation_code_black = 1
    cell_occupation_code_white = 2
    cell_occupation_code_fog = 3

    cell_piece_type_pawn = 0
    cell_piece_type_rook = 1
    cell_piece_type_knight = 2
    cell_piece_type_bishop = 3
    cell_piece_type_queen = 4
    cell_piece_type_king = 5
    cell_piece_type_promoted_pawn = 6

    # The board coordinates are in [row][col], with rows starting from the top and columns from the left
    # The pieces are printed in color with white representing the white player, red represents the black player

    def __init__(self):
        # Start with an empty board
        self.board = [[[0, 0] for x in range(
            self.board_size)] for y in range(self.board_size)]

        self.next_player = self.cell_occupation_code_white
        self.moves_until_draw = 50
        self.captured_white_pieces = []
        self.captured_black_pieces = []

    def set_from_move(self, move):
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.board[row][col][0] = move.prev_game_state.board[row][col][0]
                self.board[row][col][1] = move.prev_game_state.board[row][col][1]

        self.moves_until_draw = move.prev_game_state.moves_until_draw - 1
        self.captured_white_pieces = [piece for piece in move.prev_game_state.captured_white_pieces]
        self.captured_black_pieces = [piece for piece in move.prev_game_state.captured_black_pieces]

        for i in range(0, len(move.from_row_col), 2):
            if move.to_row_col[i] < 0 or move.to_row_col[i+1] < 0:
                self.board[move.from_row_col[i]][move.from_row_col[i+1]][0] = self.cell_occupation_code_empty
                self.board[move.from_row_col[i]][move.from_row_col[i+1]][1] = self.cell_piece_type_pawn

            if (move.prev_game_state.board[move.from_row_col[i]][move.from_row_col[i+1]][1] == self.cell_piece_type_pawn or
                move.prev_game_state.board[move.to_row_col[i]][move.to_row_col[i+1]][0] != self.cell_occupation_code_empty):
                self.moves_until_draw = 50

            if move.prev_game_state.board[move.to_row_col[i]][move.to_row_col[i+1]][0] != self.cell_occupation_code_empty:
                if move.prev_game_state.board[move.to_row_col[i]][move.to_row_col[i+1]][0] == self.cell_occupation_code_white:
                    self.captured_white_pieces.append(move.prev_game_state.board[move.to_row_col[i]][move.to_row_col[i+1]][1])
                elif move.prev_game_state.board[move.to_row_col[i]][move.to_row_col[i+1]][0] == self.cell_occupation_code_black:
                    self.captured_black_pieces.append(move.prev_game_state.board[move.to_row_col[i]][move.to_row_col[i+1]][1])

            self.board[move.to_row_col[i]][move.to_row_col[i+1]][0] = move.prev_game_state.board[move.from_row_col[i]][move.from_row_col[i+1]][0]
            self.board[move.to_row_col[i]][move.to_row_col[i+1]][1] = move.prev_game_state.board[move.from_row_col[i]][move.from_row_col[i+1]][1]

            self.board[move.from_row_col[i]][move.from_row_col[i+1]][0] = self.cell_occupation_code_empty
            self.board[move.from_row_col[i]][move.from_row_col[i+1]][1] = self.cell_piece_type_pawn

            # Pawn promotion
            if (move.to_row_col[i] == 7 and
                self.next_player == self.cell_occupation_code_black and
                self.board[move.to_row_col[i]][move.to_row_col[i+1]][1] == self.cell_piece_type_pawn):
                self.board[move.to_row_col[i]][move.to_row_col[i+1]][1] = self.cell_piece_type_promoted_pawn
            if (move.to_row_col[i] == 0 and
                self.next_player == self.cell_occupation_code_white and
                self.board[move.to_row_col[i]][move.to_row_col[i+1]][1] == self.cell_piece_type_pawn):
                self.board[move.to_row_col[i]][move.to_row_col[i+1]][1] = self.cell_piece_type_promoted_pawn

        if move.prev_game_state.next_player == self.cell_occupation_code_black:
            self.next_player = self.cell_occupation_code_white
        elif move.prev_game_state.next_player == self.cell_occupation_code_white:
            self.next_player = self.cell_occupation_code_black
        else:
            self.next_player = self.cell_occupation_code_empty

    def set_initial_state(self):
        self.board = [[[0, 0] for x in range(
            self.board_size)] for y in range(self.board_size)]

        self.board[0][0] = [self.cell_occupation_code_black,
                            self.cell_piece_type_rook]
        self.board[0][1] = [self.cell_occupation_code_black,
                            self.cell_piece_type_knight]
        self.board[0][2] = [self.cell_occupation_code_black,
                            self.cell_piece_type_bishop]
        self.board[0][3] = [self.cell_occupation_code_black,
                            self.cell_piece_type_king]
        self.board[0][4] = [self.cell_occupation_code_black,
                            self.cell_piece_type_queen]
        self.board[0][5] = [self.cell_occupation_code_black,
                            self.cell_piece_type_bishop]
        self.board[0][6] = [self.cell_occupation_code_black,
                            self.cell_piece_type_knight]
        self.board[0][7] = [self.cell_occupation_code_black,
                            self.cell_piece_type_rook]

        for i in range(self.board_size):
            self.board[1][i] = [self.cell_occupation_code_black,
                                self.cell_piece_type_pawn]
            self.board[6][i] = [self.cell_occupation_code_white,
                                self.cell_piece_type_pawn]

        self.board[7][0] = [self.cell_occupation_code_white,
                            self.cell_piece_type_rook]
        self.board[7][1] = [self.cell_occupation_code_white,
                            self.cell_piece_type_knight]
        self.board[7][2] = [self.cell_occupation_code_white,
                            self.cell_piece_type_bishop]
        self.board[7][3] = [self.cell_occupation_code_white,
                            self.cell_piece_type_king]
        self.board[7][4] = [self.cell_occupation_code_white,
                            self.cell_piece_type_queen]
        self.board[7][5] = [self.cell_occupation_code_white,
                            self.cell_piece_type_bishop]
        self.board[7][6] = [self.cell_occupation_code_white,
                            self.cell_piece_type_knight]
        self.board[7][7] = [self.cell_occupation_code_white,
                            self.cell_piece_type_rook]

        self.moves_until_draw = 50
        self.captured_white_pieces = []
        self.captured_black_pieces = []

        self.next_player = self.cell_occupation_code_white

    # def get_fogged_state(self, player):

    def get_cell_output_string(occupation_code, piece_type):

        if occupation_code == GameState.cell_occupation_code_empty:
            return '.'
        elif occupation_code == GameState.cell_occupation_code_fog:
            return '\33[90mX\033[0m'

        piece_string = ''
        if piece_type == GameState.cell_piece_type_pawn:
            piece_string = 'p'
        elif piece_type == GameState.cell_piece_type_rook:
            piece_string = 'r'
        elif piece_type == GameState.cell_piece_type_knight:
            piece_string = 'n'
        elif piece_type == GameState.cell_piece_type_bishop:
            piece_string = 'b'
        elif piece_type == GameState.cell_piece_type_queen:
            piece_string = 'q'
        elif piece_type == GameState.cell_piece_type_king:
            piece_string = 'k'
        elif piece_type == GameState.cell_piece_type_promoted_pawn:
            piece_string = 'P'

        if occupation_code == GameState.cell_occupation_code_white:
            return piece_string
        elif occupation_code == GameState.cell_occupation_code_black:
            return '\033[31m' + piece_string + '\033[0m'

    def chess_position_str_to_row_col(position_str):
        if len(position_str) != 2:
            return None

        col = -1
        if position_str[0] == 'a':
            col = 0
        elif position_str[0] == 'b':
            col = 1
        elif position_str[0] == 'c':
            col = 2
        elif position_str[0] == 'd':
            col = 3
        elif position_str[0] == 'e':
            col = 4
        elif position_str[0] == 'f':
            col = 5
        elif position_str[0] == 'g':
            col = 6
        elif position_str[0] == 'h':
            col = 7
        else:
            return None

        row = 8 - int(position_str[1])
        if row > 8 or row < 0:
            return None

        return [row, col]

    def row_col_to_chess_position_str(row, col):
        position_str = ''
        if col == 0:
            position_str = 'a'
        elif col == 1:
            position_str = 'b'
        elif col == 2:
            position_str = 'c'
        elif col == 3:
            position_str = 'd'
        elif col == 4:
            position_str = 'e'
        elif col == 5:
            position_str = 'f'
        elif col == 6:
            position_str = 'g'
        elif col == 7:
            position_str = 'h'
        else:
            return None

        position_str = position_str + str(8 - row)
        return position_str

    def is_end_of_game(self):
        if self.is_white_win() or self.is_black_win() or self.moves_until_draw == 0:
            return True
        return False

    def is_white_win(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if (self.board[row][col][0] == GameState.cell_occupation_code_black and
                    self.board[row][col][1] == GameState.cell_piece_type_king):
                    return False
        return True

    def is_black_win(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if (self.board[row][col][0] == GameState.cell_occupation_code_white and
                    self.board[row][col][1] == GameState.cell_piece_type_king):
                    return False
        return True

    def print_board(self):
        print('')
        print('  abcdefgh')
        print('')
        for row in range(self.board_size):
            print(8-row, end=' ')
            for col in range(self.board_size):
                print(GameState.get_cell_output_string(self.board[row][col][0], self.board[row][col][1]), end='')
            print(' ' + str(8-row))
        print('')
        print('  abcdefgh')
        print('')
        print('Next player: ', end='')
        if self.next_player == self.cell_occupation_code_white:
            print('white')
        else:
            print('\033[31mblack\033[0m')
        print('Moves until draw: ' + str(self.moves_until_draw))
        print('Captured white pieces: [', end='')
        for captured_white_piece in self.captured_white_pieces:
            print(GameState.get_cell_output_string(self.cell_occupation_code_white, captured_white_piece), end=',')
        print("]")

        print('Captured black pieces: [', end='')
        for captured_black_piece in self.captured_black_pieces:
            print(GameState.get_cell_output_string(self.cell_occupation_code_black, captured_black_piece), end=',')
        print("]")

    def generate_fog_of_war_state(self):

        visible_cells = set()
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col][0] == self.next_player:
                    visible_cells.add((row, col))

        moves = self.get_possible_moves()
        for move in moves:
            for i in range(0, len(move.from_row_col), 2):
                if move.to_row_col[i] >= 0 or move.to_row_col[i+1] >= 0:
                    visible_cells.add((move.to_row_col[i], move.to_row_col[i+1]))

        fog_of_war_state = GameState()
        fog_of_war_state.next_player = self.next_player
        fog_of_war_state.moves_until_draw = self.moves_until_draw

        fog_of_war_state.captured_white_pieces = []
        fog_of_war_state.captured_black_pieces = []
        for i in range(len(self.captured_white_pieces)):
            fog_of_war_state.captured_white_pieces.append(self.captured_white_pieces[i])
        for i in range(len(self.captured_black_pieces)):
            fog_of_war_state.captured_black_pieces.append(self.captured_black_pieces[i])

        for row in range(self.board_size):
            for col in range(self.board_size):
                fog_of_war_state.board[row][col][0] = self.board[row][col][0]
                fog_of_war_state.board[row][col][1] = self.board[row][col][1]
                if (row, col) not in visible_cells:
                    fog_of_war_state.board[row][col][0] = self.cell_occupation_code_fog

        return fog_of_war_state


    def get_possible_moves(self):
        moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                piece_moves = self.get_possible_moves_for_piece(row, col)
                if len(piece_moves) > 0:
                    moves += piece_moves
        return moves

    def get_possible_moves_for_piece(self, row, col):
        if self.board[row][col][0] != self.next_player:
            return []

        if self.board[row][col][1] == self.cell_piece_type_pawn:
            return self.get_pawn_moves(row, col)
        elif self.board[row][col][1] == self.cell_piece_type_rook:
            return self.get_rook_moves(row, col)
        elif self.board[row][col][1] == self.cell_piece_type_knight:
            return self.get_knight_moves(row, col)
        elif self.board[row][col][1] == self.cell_piece_type_bishop:
            return self.get_bishop_moves(row, col)
        elif self.board[row][col][1] == self.cell_piece_type_queen:
            return self.get_queen_moves(row, col)
        elif self.board[row][col][1] == self.cell_piece_type_king:
            return self.get_king_moves(row, col)
        elif self.board[row][col][1] == self.cell_piece_type_promoted_pawn:
            return self.get_promoted_pawn_moves(row, col)

    def get_pawn_moves(self, row, col):
        moves = []

        # Initial double distance move
        if (row == 1 and
           self.board[row][col][0] == self.cell_occupation_code_black and
           self.board[row+1][col][0] == self.cell_occupation_code_empty and
           self.board[row+2][col][0] == self.cell_occupation_code_empty):
            moves.append(Move(self, [row, col], [row+2,col]))
        if (row == 6 and
           self.board[row][col][0] == self.cell_occupation_code_white and
           self.board[row-1][col][0] == self.cell_occupation_code_empty and
           self.board[row-2][col][0] == self.cell_occupation_code_empty):
            moves.append(Move(self, [row, col], [row-2,col]))

        # Regular forward move
        if (row < 7 and
           self.board[row][col][0] == self.cell_occupation_code_black and
           self.board[row+1][col][0] == self.cell_occupation_code_empty):
            moves.append(Move(self, [row, col], [row+1,col]))
        if (row > 0 and
           self.board[row][col][0] == self.cell_occupation_code_white and
           self.board[row-1][col][0] == self.cell_occupation_code_empty):
            moves.append(Move(self, [row, col], [row-1,col]))

        # Capture
        if (row < 7 and col < 7 and
           self.board[row][col][0] == self.cell_occupation_code_black and
           self.board[row+1][col+1][0] == self.cell_occupation_code_white):
            moves.append(Move(self, [row, col], [row+1, col+1]))
        if (row < 7 and col > 0 and
           self.board[row][col][0] == self.cell_occupation_code_black and
           self.board[row+1][col-1][0] == self.cell_occupation_code_white):
            moves.append(Move(self, [row, col], [row+1, col-1]))
        if (row > 0 and col < 7 and
           self.board[row][col][0] == self.cell_occupation_code_white and
           self.board[row-1][col+1][0] == self.cell_occupation_code_black):
            moves.append(Move(self, [row, col], [row-1, col+1]))
        if (row > 0 and col > 0 and
           self.board[row][col][0] == self.cell_occupation_code_white and
           self.board[row-1][col-1][0] == self.cell_occupation_code_black):
            moves.append(Move(self, [row, col], [row-1, col-1]))

        return moves

    def get_rook_moves(self, row, col): #excuse me for this awfully long function
        moves=[]
        if self.next_player==self.cell_occupation_code_black: #if black player
            for i in range(row-1,-1,-1): #searches vertically, upwards
                if self.board[i][col][0] == self.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(self, [row, col], [i, col]))
                elif self.board[i][col][0] == self.cell_occupation_code_white: #capturing move
                    moves.append(Move(self, [row, col], [i, col]))
                    break
                elif self.board[i][col][0] == self.cell_occupation_code_black: #stop seaching if a black piece is found on that column
                    break
            for i in range(row+1,8,1): #searches vertically, downwards
                if self.board[i][col][0] == self.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(self, [row, col], [i, col]))
                elif self.board[i][col][0] == self.cell_occupation_code_white: #capturing move
                    moves.append(Move(self, [row, col], [i, col]))
                    break
                elif self.board[i][col][0] == self.cell_occupation_code_black: #stop seaching if a black piece is found on that column
                    break
            for i in range(col+1,8,1): #searches horizontally to the right of the piece
                if self.board[row][i][0] == self.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(self, [row, col], [row, i]))
                elif self.board[row][i][0] == self.cell_occupation_code_white: #capturing move
                    moves.append(Move(self, [row, col], [row, i]))
                    break
                elif self.board[row][i][0] == self.cell_occupation_code_black: #stop seaching if a black piece is found on that row
                    break
            for i in range(col-1,-1,-1): #searches horizontally to the left of the piece
                if self.board[row][i][0] == self.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(self, [row, col], [row, i]))
                elif self.board[row][i][0] == self.cell_occupation_code_white: #capturing move
                    moves.append(Move(self, [row, col], [row, i]))
                    break
                elif self.board[row][i][0] == self.cell_occupation_code_black: #stop seaching if a black piece is found on that row
                    break
        elif self.next_player == self.cell_occupation_code_white: #if white player
            for i in range(row-1,-1,-1): #searches vertically, upwards
                if self.board[i][col][0] == self.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(self, [row, col], [i, col]))
                elif self.board[i][col][0] == self.cell_occupation_code_black: #capturing move
                    moves.append(Move(self, [row, col], [i, col]))
                    break
                elif self.board[i][col][0] == self.cell_occupation_code_white: #stop seaching if a black piece is found on that column
                    break
            for i in range(row+1,8,1): #searches vertically, downwards
                if self.board[i][col][0] == self.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(self, [row, col], [i, col]))
                elif self.board[i][col][0] == self.cell_occupation_code_black: #capturing move
                    moves.append(Move(self, [row, col], [i, col]))
                    break
                elif self.board[i][col][0] == self.cell_occupation_code_white: #stop seaching if a black piece is found on that column
                    break
            for i in range(col+1,8,1): #searches horizontally to the right of the piece
                if self.board[row][i][0] == self.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(self, [row, col], [row, i]))
                elif self.board[row][i][0] == self.cell_occupation_code_black: #capturing move
                    moves.append(Move(self, [row, col], [row, i]))
                    break
                elif self.board[row][i][0] == self.cell_occupation_code_white: #stop seaching if a black piece is found on that row
                    break
            for i in range(col-1,-1,-1): #searches horizontally to the left of the piece
                if self.board[row][i][0] == self.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(self, [row, col], [row, i]))
                elif self.board[row][i][0] == self.cell_occupation_code_black: #capturing move
                    moves.append(Move(self, [row, col], [row, i]))
                    break
                elif self.board[row][i][0] == self.cell_occupation_code_white: #stop seaching if a black piece is found on that row
                    break
        return moves

    def get_knight_moves(self, row, col):
        moves=[]
        possibleMoves=[[row-1,col-2],[row-2,col-1],[row-1,col+2],[row-2,col+1],[row+1,col-2],[row+2,col-1],[row+1,col+2],[row+2,col+1]]
        if self.next_player == self.cell_occupation_code_black: #if black player
            for move in possibleMoves:
                if (0 <= move[0] < 8) and (0 <= move[1] < 8):
                    if self.board[move[0]][move[1]][0] == self.cell_occupation_code_empty: #non capturing move
                        moves.append(Move(self, [row, col], [move[0],move[1]]))
                    elif self.board[move[0]][move[1]][0] == self.cell_occupation_code_white: #capturing move
                        moves.append(Move(self, [row, col],[move[0],move[1]]))

        if self.next_player == self.cell_occupation_code_white: #if white player
            for move in possibleMoves:
                if (0 <= move[0] < 8) and (0 <= move[1] < 8):
                    if self.board[move[0]][move[1]][0] == self.cell_occupation_code_empty: #non capturing move
                        moves.append(Move(self, [row, col], [move[0],move[1]]))
                    elif self.board[move[0]][move[1]][0] == self.cell_occupation_code_black: #capturing move
                        moves.append(Move(self, [row, col], [move[0],move[1]]))
        return moves

    def get_bishop_moves(self, row, col):
        moves=[]
        if self.next_player == self.cell_occupation_code_black: #if black player
            for r,c in zip(range(row-1,-1,-1),range(col-1,-1,-1)): #seacrhes diag1
                if self.board[r][c][0] == self.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(self, [row, col], [r,c]))
                elif self.board[r][c][0] == self.cell_occupation_code_white: #capturing move
                    moves.append(Move(self, [row, col], [r,c]))
                    break
                elif self.board[r][c][0] == self.cell_occupation_code_black:
                    break
            for r,c in zip(range(row+1,8,1),range(col+1,8,1)): #seacrhes diag2
                if self.board[r][c][0] == self.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(self, [row, col], [r,c]))
                elif self.board[r][c][0] == self.cell_occupation_code_white: #capturing move
                    moves.append(Move(self, [row, col], [r,c]))
                    break
                elif self.board[r][c][0] == self.cell_occupation_code_black:
                    break
            for r,c in zip(range(row+1,8,1),range(col-1,-1,-1)): #seacrhes diag3
                if self.board[r][c][0] == self.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(self, [row, col], [r,c]))
                elif self.board[r][c][0] == self.cell_occupation_code_white: #capturing move
                    moves.append(Move(self, [row, col], [r,c]))
                    break
                elif self.board[r][c][0] == self.cell_occupation_code_black:
                    break
            for r,c in zip(range(row-1,-1,-1),range(col+1,8,1)): #seacrhes diag3
                if self.board[r][c][0] == self.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(self, [row, col], [r,c]))
                elif self.board[r][c][0] == self.cell_occupation_code_white: #capturing move
                    moves.append(Move(self, [row, col], [r,c]))
                    break
                elif self.board[r][c][0] == self.cell_occupation_code_black:
                    break
        if self.next_player == self.cell_occupation_code_white: #if black player
            for r,c in zip(range(row-1,-1,-1),range(col-1,-1,-1)): #seacrhes diag1
                if self.board[r][c][0] == self.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(self, [row, col], [r,c]))
                elif self.board[r][c][0] == self.cell_occupation_code_black: #capturing move
                    moves.append(Move(self, [row, col], [r,c]))
                    break
                elif self.board[r][c][0] == self.cell_occupation_code_white:
                    break
            for r,c in zip(range(row+1,8,1),range(col+1,8,1)): #seacrhes diag2
                if self.board[r][c][0] == self.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(self, [row, col], [r,c]))
                elif self.board[r][c][0] == self.cell_occupation_code_black: #capturing move
                    moves.append(Move(self, [row, col], [r,c]))
                    break
                elif self.board[r][c][0] == self.cell_occupation_code_white:
                    break
            for r,c in zip(range(row+1,8,1),range(col-1,-1,-1)): #seacrhes diag3
                if self.board[r][c][0] == self.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(self, [row, col], [r,c]))
                elif self.board[r][c][0] == self.cell_occupation_code_black: #capturing move
                    moves.append(Move(self, [row, col], [r,c]))
                    break
                elif self.board[r][c][0] == self.cell_occupation_code_white:
                    break
            for r,c in zip(range(row-1,-1,-1),range(col+1,8,1)): #seacrhes diag3
                if self.board[r][c][0] == self.cell_occupation_code_empty: #non capturing move
                    moves.append(Move(self, [row, col], [r,c]))
                elif self.board[r][c][0] == self.cell_occupation_code_black: #capturing move
                    moves.append(Move(self, [row, col], [r,c]))
                    break
                elif self.board[r][c][0] == self.cell_occupation_code_white:
                    break

        return moves

    def get_queen_moves(self, row, col):
        moves = self.get_rook_moves(row, col)
        moves += self.get_bishop_moves(row, col)
        return moves

    def get_king_moves(self, row, col):
        moves=[]
        possibleMoves=[(row-1,col-1),(row-1,col),(row-1,col+1),(row,col-1),(row,col+1),(row+1,col-1),(row+1,col),(row+1,col+1)]
        if self.next_player==self.cell_occupation_code_black: #if black player
            for move in possibleMoves:
                if (0 <= move[0] < 8) and (0 <= move[1] < 8):
                    if self.board[move[0]][move[1]][0] == self.cell_occupation_code_empty: #non capturing move
                        moves.append(Move(self, [row, col], [move[0],move[1]]))
                    elif self.board[move[0]][move[1]][0] == self.cell_occupation_code_white: #capturing move
                        moves.append(Move(self, [row, col],[move[0],move[1]]))

        if self.next_player==self.cell_occupation_code_white: #if white player
            for move in possibleMoves:
                if (0 <= move[0] < 8) and (0 <= move[1] < 8):
                    if self.board[move[0]][move[1]][0] == self.cell_occupation_code_empty: #non capturing move
                        moves.append(Move(self, [row, col], [move[0],move[1]]))
                    elif self.board[move[0]][move[1]][0] == self.cell_occupation_code_black: #capturing move
                        moves.append(Move(self, [row, col], [move[0],move[1]]))
        return moves

    def get_promoted_pawn_moves(self, row, col):
        return self.get_queen_moves(row, col)

if __name__ == "__main__":
    game_state = GameState()
    game_state.set_initial_state()

    while True:
        game_state.generate_fog_of_war_state().print_board()

        moves = game_state.get_possible_moves()
        print("Select a move: ")
        for i in range(len(moves)):
            print(str(i) + ': ' +  GameState.row_col_to_chess_position_str(moves[i].from_row_col[0], moves[i].from_row_col[1]) + ' -> ' +
                    GameState.row_col_to_chess_position_str(moves[i].to_row_col[0], moves[i].to_row_col[1]))
        move_index = int(input())
        game_state.set_from_move(moves[move_index])
