from GameState import Move, GameState
import heuristic


game_state = GameState()
game_state.set_initial_state()


def play_game(white_player, black_player):
    game_state = GameState()
    game_state.set_initial_state()

    while not game_state.is_end_of_game():
        moves = game_state.get_possible_moves()
        move = None
        if game_state.next_player == GameState.cell_occupation_code_black:
            move = black_player.play(game_state, moves)
        else:
            move = white_player.play(game_state, moves)
        game_state.set_from_move(move)

    if game_state.is_white_win():
        return white_player
    elif game_state.is_black_win():
        return black_player
    return None

if __name__ == "__main__":
    white_player = Player(True, GameState.cell_occupation_code_white, None)
    black_player = Player(True, GameState.cell_occupation_code_black, None)

    winner = play_game(white_player, black_player)
    if winner is white_player:
        print("You won!")
    elif winner is black_player:
        print("You lost!")
    else:
        print("It's a draw!")