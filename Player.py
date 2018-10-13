from GameState import Move, GameState
from heuristic import h, heuristic_weights_shape
import random
import numpy

class Player:
    def __init__(self, is_ai_player, player_id, heuristic_weights):
        self.is_ai_player = is_ai_player
        self.player_id = player_id
        self.heuristic_weights = heuristic_weights

        # Generate random weights if no weights are provided
        if heuristic_weights is None:
            self.heuristic_weights = numpy.array([
                [
                    random.uniform(0,1) for _ in range(heuristic_weights_shape()[1])
                ] for __ in range(heuristic_weights_shape()[0])
            ])

    def play(self, game_state, possible_moves):
        if self.is_ai_player:
            best_score = -1000000
            best_move = None
            for move in possible_moves:
                next_state = GameState()
                fogged_move = Move(game_state.generate_fog_of_war_state(), 
                                        [move.from_row_col[0], move.from_row_col[1]], 
                                        [move.to_row_col[0], move.to_row_col[1]])
                next_state.set_from_move(fogged_move)
                move_score = h(next_state, self.heuristic_weights)
                if move_score > best_score:
                    best_score = move_score
                    best_move = move
            return best_move
        else:
            game_state.generate_fog_of_war_state().print_board()
            print("Select a move: ")
            for i in range(len(possible_moves)):
                print(str(i) + ': ' +
                    GameState.row_col_to_chess_position_str(possible_moves[i].from_row_col[0],
                                                            possible_moves[i].from_row_col[1]) +
                    ' -> ' +
                    GameState.row_col_to_chess_position_str(possible_moves[i].  to_row_col[0],
                                                            possible_moves[i].  to_row_col[1]))
            move_index = int(input())
            return possible_moves[move_index]
