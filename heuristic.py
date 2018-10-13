from GameState import GameState
import math
import numpy

def player_heuristic(game_state, player):
    number_of_pieces = 0
    for row in range(game_state.board_size):
        for col in range(game_state.board_size):
            if game_state.board[row][col][0] == player:
                number_of_pieces += 1
    return float(number_of_pieces)/32 #normalise the output

def heuristic_A(game_state):
    other_player = GameState.cell_occupation_code_empty
    if game_state.next_player == GameState.cell_occupation_code_white:
        other_player = GameState.cell_occupation_code_black
    elif game_state.next_player == GameState.cell_occupation_code_black:
        other_player = GameState.cell_occupation_code_white

    return player_heuristic(game_state, game_state.next_player) - player_heuristic(game_state, other_player)

# TODO : insert definition of heuristics here

# The same heuristics are going to be used by each player,
# it's therefore a constant
HEURISTICS = [
    heuristic_A,
    heuristic_A
    #heuristicB,
    #heuristicC,
    # ...
]

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
