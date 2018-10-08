# for colorful printing
from ansimarkup import ansiprint as print
from Move import Move

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
    
    def set_from_move(self, move):
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.board[row][col] = move.prev_game_state.board[row][col]
        
        for i in range(0, len(move.from_row_col), 2):
            if move.to_row_col[i] < 0 or move.to_row_col[i+1] < 0:
                self.board[move.from_row_col[i]][move.from_row_col[i+1]][0] = self.cell_occupation_code_empty
                self.board[move.from_row_col[i]][move.from_row_col[i+1]][1] = self.cell_piece_type_pawn
            
            self.board[move.to_row_col[i]][move.to_row_col[i+1]][0] = move.prev_game_state.board[move.from_row_col[i]][move.from_row_col[i+1]][0]
            self.board[move.to_row_col[i]][move.to_row_col[i+1]][1] = move.prev_game_state.board[move.from_row_col[i]][move.from_row_col[i+1]][1]

            self.board[move.from_row_col[i]][move.from_row_col[i+1]][0] = self.cell_occupation_code_empty
            self.board[move.from_row_col[i]][move.from_row_col[i+1]][1] = self.cell_piece_type_pawn
        
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

        self.next_player = self.cell_occupation_code_white

    # def get_fogged_state(self, player):

    def get_cell_output_string(self, row, col):
        occupation_code = self.board[row][col][0]
        piece_type = self.board[row][col][1]

        if occupation_code == self.cell_occupation_code_empty:
            return '.'
        elif occupation_code == self.cell_occupation_code_fog:
            return 'X'

        piece_string = ''
        if piece_type == self.cell_piece_type_pawn:
            piece_string = 'p'
        elif piece_type == self.cell_piece_type_rook:
            piece_string = 'r'
        elif piece_type == self.cell_piece_type_knight:
            piece_string = 'n'
        elif piece_type == self.cell_piece_type_bishop:
            piece_string = 'b'
        elif piece_type == self.cell_piece_type_queen:
            piece_string = 'q'
        elif piece_type == self.cell_piece_type_king:
            piece_string = 'k'
        elif piece_type == self.cell_piece_type_promoted_pawn:
            piece_string = 'P'

        if occupation_code == self.cell_occupation_code_white:
            return piece_string
        elif occupation_code == self.cell_occupation_code_black:
            return '<red>' + piece_string + '</red>'

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

    def print_board(self):
        print('')
        print('  abcdefgh')
        print('')
        for row in range(self.board_size):
            print(8-row, end=' ')
            for col in range(self.board_size):
                print(self.get_cell_output_string(row, col), end='')
            print(' ' + str(8-row))
        print('')
        print('  abcdefgh')
        print('')

if __name__ == "__main__":
    game_state = GameState()
    game_state.set_initial_state()

    while True:
        game_state.print_board()

        moves = Move.get_possible_moves(game_state)
        print("Select a move: ")
        for i in range(len(moves)):
            print(str(i) + ': ' +  GameState.row_col_to_chess_position_str(moves[i].from_row_col[0], moves[i].from_row_col[1]) + ' -> ' + 
                    GameState.row_col_to_chess_position_str(moves[i].to_row_col[0], moves[i].to_row_col[1]))
        move_index = int(input())
        game_state.set_from_move(moves[move_index])