import numpy
import random
from threading import Thread
from math import tanh

from GameState import GameState
from heuristic import HEURISTICS
import Player
from play_game import play_game
# GLOBAL VARIABLES
# genes and precision
WEIGHT_PRECISION = 32 # bit float precison, also the number of bits in each gene
MUTATION_STRENGTH = 5 # the average number of bits that will flip in each gene
B_ORDER = 0  # DEPRECATED order of the Bernstein basis
# Population fitting
MEAN_CUT_SELECTION = .5 # ration for the mean transition for the natural selection in the population
SPREAD_CUT_SELECTION = .3 # the spread

def set_bit(bit, value):
    return value | (1<<bit)

def clear_bit(bit, value):
    return value & ~(1<<bit)

def flip_bit(bit, value):
    return value ^ (1<<bit)

def get_bit(bit, value):
    return (value & (1<<bit))>>bit

class Chromosome:
    def __init__(self, genes = numpy.array([])):
        self.genes = genes
        self.length = self.genes.size

    def __repr__(self):
        str = ':'.join(format(g, '08x') for g in self.genes)
        return str

    def __str__(self):
        binary = ':'.join(format(g, '032b') for g in self.genes)
        str = "Chrom hex : "+repr(self) #+" bin: "+binary
        return str

    def fromStr(str):
        Str = str.split(':')
        return Chromosome(numpy.array([int(s, 16) for s in Str]))

    #static
    def weight_to_gene(w):
        return int(w*2**WEIGHT_PRECISION)

    def set_gene(self, w, index):
        self.genes[index] = weight_to_gene(w)

    def set_genes(self, weights):
        self.genes = (
            weights.reshape(weights.size)*2**WEIGHT_PRECISION
        ) . astype(int)
        self.length = weights.size

    def to_weights(self, bernstein_basis_order):
        # the basis order + 1 has to divide the number of genes
        m = bernstein_basis_order + 1 #the number of polynomes
        return self.genes.reshape(self.length//m,m).astype(float)/2**WEIGHT_PRECISION

    def mutate_bit(self, f_bit, bit):
        gene_index = bit//WEIGHT_PRECISION
        bit = bit%WEIGHT_PRECISION
        self.genes[gene_index] = f_bit(bit, self.genes[gene_index])
        return self.genes[gene_index]

    def random_mutations(self, bernstein_basis_order):
        length = self.length*WEIGHT_PRECISION
        if length == 0 :
            return
        p = float(MUTATION_STRENGTH)/WEIGHT_PRECISION
        # cout = 0
        for i in range(length) :
            q = random.uniform(0, 1)
            if(q < p):
                self.mutate_bit(flip_bit, i)
                # cout +=1
        # print("bits flipped : ", cout)
        # Edge case scenario : normalise the n-1 first weights
        weights = self.to_weights(bernstein_basis_order)
        for j in range(weights.shape[1]):
            W_h_sum = weights[:,j].sum()
            if W_h_sum >= 1:
                weights[:,j] /= W_h_sum
        self.set_genes(weights)

class Individual:
    """ An individual in the evolving population """
    def __init__(self, chromosomes, bernstein_basis_order = 0, dominant_chromosome = random.randint(0,1), score = -1):
        """
        :param chromosomes: the parent's set of chromosomes
        :param dominant_chromosome: the index of the chromosome that will express itself
        """
        self.chromosomes = chromosomes
        self.dom = chromosomes[dominant_chromosome]
        self.basis_n = bernstein_basis_order
        self.score = score
        self.alive = True


    def __repr__(self):
        str = 'b.{}$s.{}$a.'.format(self.basis_n, self.score)
        if self.alive:
            str += '1'
        else:
            str += '0'
        for c in self.chromosomes:
            if c is self.dom:
                str += "$dom."+repr(c)
            else:
                str += "$dis."+repr(c)
        return str

    def __str__(self):
        str = 'Individual '
        l = 0
        for c in self.chromosomes:
            if l == 1:
                str += '\n           '
            if c is self.dom:
                str += "chrom {} : {} <-dominant".format(l, repr(c))
            else:
                str += "chrom {} : {}".format(l, repr(c))
            l = 1
        return str

    def fromStr(str):
        Str = str.split('$')
        chroms = []
        dom = 0
        s = Str.pop(0)
        basis = int( s.split('.')[1])
        s = Str.pop(0)
        score = int( s.split('.')[1])
        s = Str.pop(0)
        alive =  s.split('.')[1] == '1'
        for k, s in enumerate(Str):
            ss = s.split('.')
            if ss[0] == 'dom':
                chroms.append(Chromosome.fromStr(ss[1]))
                dom = k
            else:
                chroms.append(Chromosome.fromStr(ss[1]))
        ret =  Individual(chroms, basis, dom, score)
        ret.alive = alive
        return ret

    def get_weights(self, compressed = True):
        if(compressed):
            return self.dom.to_weights(self.basis_n)
        else:
            w = self.dom.to_weights(self.basis_n)
            w_n = numpy.array([ [
                1 - w[:,j].sum() for j in range(w.shape[1])
            ] ])
            return numpy.concatenate((w, w_n), axis=0)

    def mate_with(self, partner):
        chromosomes = [
            self   .chromosomes[random.randint(0,1)],
            partner.chromosomes[random.randint(0,1)]
        ]
        for chromosome in chromosomes:
            chromosome.random_mutations(self.basis_n)
        return Individual(chromosomes, self.basis_n)

    def get_player(self, player_id):
        return Player.Player(True, player_id, self.get_weights(False))

class Population:
    def __init__(self, individuals, generation = 0):
        self.individuals = individuals
        self.generation = generation
        self.size   = len(self.individuals)
        self.length = len(self.individuals)

    def __repr__(self):
        str = 'population generation :{}\n'.format(self.generation)
        str += '\n'.join(repr(i) for i in self.individuals)
        return str

    def __radd__(self, other):
        return Population(self.individuals+other.individuals)

    def __add__(self, other):
        return Population(self.individuals+other.individuals)

    def fromStr(str):
        Str = str.split('\n')
        generation = int(Str[0].split(':')[1])
        Str.pop(0)
        indiv = []
        for s in Str:
            indiv.append(Individual.fromStr(s))
        return Population(indiv, generation)

    def compete(self, point_reset = False , threaded = False, n_threads = -1):
        """
            Every individual competes in dark chess and gets a final score distributed as such :
                + 3 per win
                + 1 per draw
                + 0 per loss
        """
        if point_reset:
            print("Reinitialising each players scores")
            for i in self.individuals:
                i.score = 0
        nb_faceoffs = self.size*(self.size-1)//2
        cout = 0
        if threaded:
            from pathos.multiprocessing import ProcessingPool as Pool
            from multiprocessing import cpu_count
            if n_threads < 0:
                nr_threads = cpu_count()//2 # that is usually the number of physical cores
            else:
                nr_threads = n_threads
            print("Starting competition with {} threads".format(nr_threads))

            def syncGame(pair):
                p1, p2 = pair
                winner = play_game(p1,p2)
                if winner is p1:
                    return [3,0]
                elif winner is p2:
                    return [0,3]
                else:
                    return [1,1]

            player_pairs = []
            # scoreLock = multiprocessing.RLock()
            p = Pool(nr_threads)
            for k1, i1 in enumerate(self.individuals):
                for k2, i2 in enumerate(self.individuals):
                    if k1<k2:
                        player_pairs.append([
                            i1.get_player(GameState.cell_occupation_code_white),
                            i2.get_player(GameState.cell_occupation_code_black)
                        ])
            res = p.map(syncGame, player_pairs)
            len_i = len(self.individuals)
            cout = 0
            for i in range(len_i):
                for j in range(i+1, len_i):
                    self.individuals[i].score+=res[cout][0]
                    self.individuals[j].score+=res[cout][1]
                    cout+=1
        else:
            print("Starting competition")
            for k1, i1 in enumerate(self.individuals):
                for k2, i2 in enumerate(self.individuals):
                    if k2>k1:
                        cout += 1
                        print ( "competition underway : {}% [".format(int(100*cout/nb_faceoffs))+"#"*cout+"-"*(nb_faceoffs-cout)+"]", end='\r')
                        p1 = i1.get_player(GameState.cell_occupation_code_white)
                        p2 = i2.get_player(GameState.cell_occupation_code_black)
                        winner = play_game(p1,p2)
                        if winner is p1:
                            i1.score += 3
                            i2.score += 0
                        elif winner is p2:
                            i1.score += 0
                            i2.score += 3
                        else:
                            i1.score += 1
                            i2.score += 1
            print('') # gets rid of the carriage return char

    def everybodyCompetes(populations, point_reset = True, threaded = False, n_threads = -1):
        if point_reset:
            for pop in populations:
                print("Reinitialising each players scores")
                for i in pop.individuals:
                    i.score = 0
        for k1, pop1 in enumerate(populations):
            for k2, pop2 in enumerate(populations):
                if k1 > k2 :
                    pop = pop1 + pop2
                    pop.compete(False, threaded, n_threads)
                    l1, l2 = len(pop1), len(pop2)
                    pop1 = [i for i in pop[ 0 : l1   ]]
                    pop2 = [i for i in pop[l1 : l1+l2]]

    def naturalySelect(self):
        self.individuals.sort(key= lambda i : i.score)
        max_score = self.individuals[-1].score
        def transition_f(m, s):
            # m : mean
            # s: spread / standard deviation
            # https://en.wikipedia.org/wiki/Logistic_distribution
            return lambda _x : .5 + .5*tanh( (_x-m)/2/s )

        f_t = transition_f(MEAN_CUT_SELECTION, SPREAD_CUT_SELECTION)
        deathToll = 0
        for k in range(len(self.individuals)):
            q = f_t(self.individuals[k].score/max_score)
            p = random.uniform(0,1)
            if p > q :
                self.individuals[k].alive = False
                deathToll += 1
        self.individuals = [i for i in self.individuals if i.alive]
        return deathToll

    def naturalyRenew(self, deathToll):
        # it is assumed that self.individuals is sorted from worst to best score
        birthCount = 0
        new_individuals = []
        mating = [False]*len(self.individuals)
        max_score = self.individuals[-1].score
        while birthCount < deathToll:
            for k1, i1 in enumerate(self.individuals):
                if birthCount >= deathToll:
                    break
                for k2, i2 in enumerate(self.individuals):
                    if birthCount >= deathToll:
                        break
                    elif (k1 > k2) and (not mating[k1]) and (not mating[k2]):
                        q = i1.score*i2.score/max_score**2
                        p = random.uniform(0,1)**2
                        if p < q :
                            mating[k1] = True
                            mating[k2] = True
                            birthCount += 1
                            new_individuals.append(i1.mate_with(i2))
            mating = [False]*len(self.individuals)
        self.individuals.extend(new_individuals)
        return new_individuals


# This is ugly, but synchronous computation won't work otherwise



if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Make two Individuals play against each other.')
    parser.add_argument('-n', type=int, default=0,
                        help='order of the Bernstein base (default: 0)')
    parser.add_argument('-i', type=int, default=2,
                        help='number of individuals in the population')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                     const=sum, default=max,
    #                     help='sum the integers (default: find the max)')
    args = parser.parse_args()
    pol_n = args.n+1 #number of polynomes
    individuals = [ Individual([Chromosome(), Chromosome()], args.n) for _ in range(args.i) ]
    print("number of heuristics implemented : ", len(HEURISTICS))
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
        print(indiv)

    print("\nwill play against each other : ")
    pop = Population(individuals)
    pop.compete()
    print("Results of the competition :")
    for i in pop.individuals:
        print(i, " obtained score : ", i.score)
    print("\nnow there will be an offering to the blood gods!\n\n     Let the fittest survive!\n")
    deathToll = pop.naturalySelect()
    if deathToll == 0:
        print("\nNo AIs died! Do they all have the same score??\n")
    print("These are the scores of the surviving AIs after the loss of ", deathToll, " innocent AIs :")
    for i in pop.individuals:
        if i.alive:
            print(" score : ", i.score)
    print("proceeding forth with a thorough copulation to compensate for the recent genocide")
    new_individs = pop.naturalyRenew(deathToll)
    print("Newborns :")
    for indiv in new_individs:
        print(indiv)

    # print(args.accumulate(args.integers))
