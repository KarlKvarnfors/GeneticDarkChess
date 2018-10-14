from play_game import play_game
from GameState import GameState
from Player import Player
from Lineage import Lineage


def play_against_lineage(lineage_file):
    lineage = Lineage.fromFile(lineage_file)
    black_player = lineage.populations[-1].individuals[-1].get_player(GameState.cell_occupation_code_black)
    white_player = Player(False, GameState.cell_occupation_code_white, None)

    winner = play_game(white_player, black_player)
    if winner is white_player:
        print("You won!")
    elif winner is black_player:
        print("You lost!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    lineage_file = input("Lineage file name: ")
    play_against_lineage(lineage_file)

