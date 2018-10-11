import numpy
import random
# global variables
WEIGHT_PRECISION = 32 # bit float precison, also the number of bits in each gene
MUTATION_STRENGTH = 5 # the average number of bits that will flip in each gene
B_ORDER = 2 # order of the Bernstein basis

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
            weights.reshape(1,weights.size)[0]*2**WEIGHT_PRECISION
        ) . astype(int)
        self.length = weights.size

    def to_weights(self):
        m = B_ORDER
        return numpy.array([
            self.genes[i*m:(i+1)*m].astype(float)/2**WEIGHT_PRECISION
            for i in range(self.length/m)
        ])

    def mutate_bit(self, f_bit, bit):
        gene_index = bit//WEIGHT_PRECISION
        bit = bit%WEIGHT_PRECISION
        self.genes[gene_index] = f_bit(bit, self.genes[gene_index])
        return self.genes[gene_index]

    def random_mutations(self):
        length = self.length*WEIGHT_PRECISION
        p = float(MUTATION_STRENGTH)/WEIGHT_PRECISION
        # cout = 0
        for i in range(length) :
            q = random.uniform(0, 1)
            if(q < p):
                self.mutate_bit(flip_bit, i)
                # cout +=1
        # print "bits flipped : ", cout
        # Edge case scenario : normalise the n-1 first weights
        weights = self.to_weights()
        for j in range(weights.shape[1]):
            W_h_sum = weights[:,j].sum()
            if W_h_sum >= 1:
                weights[:,j] /= W_h_sum
        self.set_genes(weights)

class Individual:
    """ An individual in the evolving population """
    def __init__(self, chromosomes, dominant_chromosome = random.randint(0,1)):
        """
        :param chromosomes: the parent's set of chromosomes
        :param dominant_chromosome: the index of the chromosome that will express itself
        """
        self.chromosomes = chromosomes
        self.dom = chromosomes[dominant_chromosome]

    def get_weights(self):
        return self.dom.to_weights()

    def mate(self, partner):
        chromosomes = [
            self   .chromosomes[random.randint(0,1)].random_mutations(),
            partner.chromosomes[random.randint(0,1)].random_mutations()
        ]
        return Individual(chromosomes)
