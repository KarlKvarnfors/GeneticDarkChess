from GameState import GameState

def player_heuristic(game_state, weights, player):
    number_of_pieces = 0
    for row in range(game_state.board_size):
            for col in range(game_state.board_size):
                if game_state.board[row][col][0] == player:
                    number_of_pieces += 1

    return weights[0] * number_of_pieces

def heuristic(game_state, weights):
    other_player = GameState.cell_occupation_code_empty
    if game_state.next_player == GameState.cell_occupation_code_white:
        other_player = GameState.cell_occupation_code_black
    elif game_state.next_player == GameState.cell_occupation_code_black:
        other_player = GameState.cell_occupation_code_white

    return player_heuristic(game_state, weights, game_state.next_player) - player_heuristic(game_state, weights, other_player)

def number_of_heuristic_weights():
    return 1
