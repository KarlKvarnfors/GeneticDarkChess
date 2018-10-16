import sys
import time
import random
import numpy

from genetics import Individual, Chromosome, Population, HEURISTICS
from Lineage import Lineage


def main(pol_n, len_i, len_g, lin_n, regen, n_threads):

    THREADED = n_threads > 0
    THREADS = n_threads

    def lineageName(pol_n, gen_n):
        return "test/BernBase{}gen{}.lineage".format(pol_n, gen_n)

    #********** Generate the asked number of generations *********
    #   check

    if(regen):
        lin_n = pol_n
        lins = []
        # l is an int here
        individuals = [ Individual([Chromosome(), Chromosome()], pol_n-1) for _ in range(len_i) ]
        for indiv in individuals:
            for c in indiv.chromosomes:
                # generate a random set of weights for the chromosome
                weights_compressed = [[0]*pol_n]* (len(HEURISTICS)-1)
                for W_h in weights_compressed:
                    tmp_w = [0]*pol_n
                    for i in range(pol_n):
                        W_h[i] = max(0,1 -random.random() -tmp_w[i])
                        tmp_w[i] = tmp_w[i] + W_h[i]
                c.set_genes(numpy.array(weights_compressed))
        pop = Population(individuals, 1)
        print("First generation created for lineage number ", lin_n)
        lins.append(Lineage([pop], "0"))
        fname = lineageName(pol_n, lins[0].generations)
        print("saving to file : ", fname)
        lins[0].toFile(fname)

        # l is a lineage here
        for l in lins:
            while l.generations < len_g:
                print("Creating generation ",l.generations+1)
                l.nextGeneration(THREADED, THREADS)
                fname = lineageName(pol_n, l.generations)
                print("saving to file : ", fname)
                l.toFile(fname)
        lin = lins[-1]
    else:
        for g in range(len_g, 0, -1):
            try:
                fname = lineageName(pol_n, g)
                fh = open(fname, 'r')
                # Store configuration file values
                lin = Lineage.fromFile(fname)
                break
            except FileNotFoundError:
                if(g <= 1):
                    print("No previous generations were found, please add the -r or --regenerate flag")
                    exit("no files found : "+lineageName("<Bernstein base>", "<generationNumber>"))
    # print(lin)
    lin.beatYourElders(5, True, True, True, n_threads)
    # Lineage.plotScorePerGeneration(lin.populations)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Test the algorithm for a given number of generations.')
    parser.add_argument('-n', type=int, default=0,
                        help='order of the Bernstein base (default: 0)')
    parser.add_argument('-i', type=int, default=2,
                        help='number of individuals in the population (default: 2)')
    parser.add_argument('-g', type=int, default=2,
                        help='number of succeeding generations (default: 2)')
    parser.add_argument('-l', type=int, default=1,
                        help='number of different lineages (default: 1)')
    parser.add_argument('-t', '--threads', type=int, default=-1,
                        help='number of different lineages (default: -1, non threaded)')
    parser.add_argument('-r', "--regenerate", action="store_true",
                        help="Regenerates the lineage from start (default : tries to load from file)")
    args = parser.parse_args()

    main(args.n+1, args.i, args.g, args.l, args.regenerate, args.threads)
