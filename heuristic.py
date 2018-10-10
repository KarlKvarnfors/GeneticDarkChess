from GameState import GameState
import math

def player_heuristic(game_state, weights, player):
    number_of_pieces = 0
    for row in range(game_state.board_size):
            for col in range(game_state.board_size):
                if game_state.board[row][col][0] == player:
                    number_of_pieces += 1

    return weights[0] * number_of_pieces

# returns the k-th bernstein polynomial in base n
def bernstein(k, n):
	return lambda x : nCr(n,k) * (x**k) * ( (1-x)**(n-k) )

def bernsteinweight_per_heuristic(nr_of_pieces, basis, degree):
    t=nr_of_pieces/32
    #assuming the bernstein basis is 3:
    b=basis
    d=degree
    bernsteinweight = bernstein(b, d)
    return bernsteinweight(t)

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)


def heuristic(game_state, weights):
    other_player = GameState.cell_occupation_code_empty
    if game_state.next_player == GameState.cell_occupation_code_white:
        other_player = GameState.cell_occupation_code_black
    elif game_state.next_player == GameState.cell_occupation_code_black:
        other_player = GameState.cell_occupation_code_white

    return player_heuristic(game_state, weights, game_state.next_player) - player_heuristic(game_state, weights, other_player)

def number_of_heuristic_weights():
    return 1
