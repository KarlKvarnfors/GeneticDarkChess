from Lineage import Lineage



if __name__ == "__main__":
    import argparse
    import sys
    from genetics import Individual, Chromosome
    from heuristic import HEURISTICS
    import random
    import numpy
    import time

    # parser = argparse.ArgumentParser(description='Plot the changes in performance in a given lineage.')
    # parser.add_argument('-f', type=str,
    #                     help='file to load')
    # args = parser.parse_args()
    # print(args.f, type(args.f))
    lin = Lineage.fromFile("test/lin0gen2.lineage")
    # lin.beatYourElders(3, False, True, True, 2)
    Lineage.plot(lin.populations)
