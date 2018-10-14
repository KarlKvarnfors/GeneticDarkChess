from genetics import Population

class Lineage:
    def __init__(self, populations = [], name = ''):
        self.populations = populations
        self.name = name
        self.generations = len(self.populations)
        self.length = len(self.populations)
        self.size = len(self.populations)

    def __repr__(self):
        str = 'LINEAGE {}\n\n'.format(self.name)
        str += '\n\n'.join(repr(pop) for pop in self.populations)
        return str

    def fromStr(str):
        Str = str.split('\n\n')
        name = Str.pop(0).split(' ')[1]
        pops = [Population.fromStr(s) for s in Str]
        return Lineage(pops, name)

    def toFile(self, filename = "a.lin"):
        f = open(filename, 'w')
        f.write(repr(self))
        return f.close()

    def fromFile(filename):
        f = open(filename,'r')
        lin = Lineage.fromStr(f.read())
        f.close()
        return lin

    def updtLen(self):
        self.generations = len(self.populations)
        self.length = len(self.populations)
        self.size = len(self.populations)

    def nextGeneration(self, threaded = False):
        popul = Population(self.populations[-1].individuals, self.generations+1)
        t1 = time.time()
        popul.compete(threaded)
        delta = time.time() - t1
        print("delta: {}".format(delta))
        deaths = popul.naturalySelect()
        popul.naturalyRenew(deaths)
        self.populations.append(popul)
        self.updtLen()
        return popul


if __name__ == "__main__":
    import argparse
    import sys
    from genetics import Individual, Chromosome
    from heuristic import HEURISTICS
    import random
    import numpy
    import time

    parser = argparse.ArgumentParser(description='Make two Individuals play against each other.')
    parser.add_argument('-n', type=int, default=0,
                        help='order of the Bernstein base (default: 0)')
    parser.add_argument('-i', type=int, default=2,
                        help='number of individuals in the population (default: 2)')
    parser.add_argument('-g', type=int, default=2,
                        help='number of succeeding generations (default: 2)')
    parser.add_argument('-l', type=int, default=1,
                        help='number of different lineages (default: 1)')

args = parser.parse_args()
pol_n = args.n+1 #number of polynomes

lins = []

# l is an int here
for l in range(args.l):
    individuals = [ Individual([Chromosome(), Chromosome()], args.n) for _ in range(args.i) ]
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
    print("First generation created for lineage number ", l)
    lins.append(Lineage([pop], str(l)))

# l is a lineage here
for l in lins:
    while l.generations < args.g:
        print("Creating generation ",l.generations+1)
        l.nextGeneration(True)
        fname = "lin{}gen{}.lineage".format(l.name, l.generations)
        print("saving to file : ", "test/"+fname)
        l.toFile("test/"+fname)
