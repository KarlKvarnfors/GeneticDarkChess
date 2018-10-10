import numpy
from functools import reduce
import math
# global variables
WEIGHT_PRECISION = 32 # bit float precison

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

	def to_weights(self, polynome_basis_order = 1):
		m = polynome_basis_order
		return numpy.array([
			self.genes[i*m:(i+1)*m].astype(float)/2**WEIGHT_PRECISION
			for i in range(self.length/m)
		])

	def manip_bit(self, f_bit, bit):
		gene_index = bit//WEIGHT_PRECISION
		bit = bit%WEIGHT_PRECISION
		self.genes[gene_index] = f_bit(bit, self.genes[gene_index])
		return self.genes[gene_index]


#
# @parameter player
class Individual:
	"""
		an individual in the evolving population
		:param weights: numpy array[float], the array of weigths.   dim = 1 -> no polynomial adjustment
																	dim = 2 -> polynomial adjustment
    """
	def __init__(self, weights):
		self.weights = weights


	# def getGenes
