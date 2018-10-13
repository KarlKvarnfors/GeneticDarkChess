import numpy
import random
from heuristic import HEURISTICS
import Player
# global variables
WEIGHT_PRECISION = 32 # bit float precison, also the number of bits in each gene
MUTATION_STRENGTH = 5 # the average number of bits that will flip in each gene
B_ORDER = 0  # order of the Bernstein basis

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
        self.length = self.genes.shape[0]

    #static
    def weight_to_gene(self, w):
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
        return self.genes.reshape(self.length/m,m).astype(float)/2**WEIGHT_PRECISION

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
        # print "bits flipped : ", cout
        # Edge case scenario : normalise the n-1 first weights
        weights = self.to_weights(bernstein_basis_order)
        for j in range(weights.shape[1]):
            W_h_sum = weights[:,j].sum()
            if W_h_sum >= 1:
                weights[:,j] /= W_h_sum
        self.set_genes(weights)

class Individual:
    """ An individual in the evolving population """
    def __init__(self, chromosomes, bernstein_basis_order = 0, dominant_chromosome = random.randint(0,1)):
        """
        :param chromosomes: the parent's set of chromosomes
        :param dominant_chromosome: the index of the chromosome that will express itself
        """
        self.chromosomes = chromosomes
        self.dom = chromosomes[dominant_chromosome]
        self.basis_n = bernstein_basis_order

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
            self   .chromosomes[random.randint(0,1)].random_mutations(),
            partner.chromosomes[random.randint(0,1)].random_mutations()
        ]
        return Individual(chromosomes)

    def get_player(self, player_id):
        return Player.Player(True, player_id, self.get_weights(False))

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Make two Individuals play against each other.')
    parser.add_argument('-n', type=int, default=0,
                        help='order of the Bernstein base (default: 0)')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                     const=sum, default=max,
    #                     help='sum the integers (default: find the max)')

    args = parser.parse_args()
    pol_n = args.n+1 #number of polynomes
    individuals = [ Individual([Chromosome(),
                                Chromosome()],
                                args.n),
                    Individual([Chromosome(),
                                Chromosome()],
                                args.n)         ]
    print "number of heuristics implemented : ", len(HEURISTICS)
    print "number of individuals who are going to play against each other : ",len(individuals)
    for indiv in individuals:
        print "\nindividual ", indiv
        for chromosome in indiv.chromosomes:
            # generate a random set of weights for the chromosome
            weights_compressed = [[0]*pol_n]* (len(HEURISTICS)-1)
            for W_h in weights_compressed:
                tmp_w = [0]*pol_n
                for i in range(pol_n):
                    W_h[i] = max(0,1 -random.random() -tmp_w[i])
                    tmp_w[i] = tmp_w[i] + W_h[i]
            chromosome.set_genes(numpy.array(weights_compressed))
            print "with chromosome weights : ",chromosome.to_weights(args.n)

    print "\nwill play against each other : "

    import play_game
    from GameState import GameState
    print GameState.cell_occupation_code_white
    print GameState.cell_occupation_code_black
    print individuals[0]
    print individuals[1]
    winner = play_game.play_game (  individuals[0].get_player(GameState.cell_occupation_code_white) ,
                                    individuals[1].get_player(GameState.cell_occupation_code_black) )
    if winner is white_player:
        print("individual 1 won!")
    elif winner is black_player:
        print("individual 2 won!")
    else:
        print("It's a draw!")
    # print args.accumulate(args.integers)
