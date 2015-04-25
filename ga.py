from math import *
from random import *
from sys import *
from game import *
from phase_ann2 import *

# This file is used to generate the AI file through tournament selection
# and an evolutionary program.

def create_ann():
	return phase_ann(4, 4, 4, 3, 3)


# starts running tournament selection to improve the weight sets given
# sorts them by rank and returns them
def run_tournament_selection(anns, n, max_iterations):
	wincounts = [0] * len(anns)
	runnerupcounts = [0] * len(anns) # use for tie breaking
	for i in range(0, max_iterations):
		# select three random anns
		# run a single 3-AI game and get the winner and runner-up.  increment the values in the wincount and runnerupcount arrays
		a = randrange(0, len(anns))
		b = randrange(0, len(anns))	
		c = randrange(0, len(anns))	
		while a == b or b == c or a == c:
			a = randrange(0, len(anns))
			b = randrange(0, len(anns))	
			c = randrange(0, len(anns))
	
	# return [an n-length of weightsets indecies sorted by their wincount values, an n-length of weightsets indecies sorted by their runnerupcount values]

	pass

# fills a new population with mates, fits, mutates and returns it
def mate_population(population, n, mutation_rate):
	children = []
	for i in range(0, n):
		a = randrange(0, len(population))
		b = randrange(0, len(population))		
		while a == b:  # make sure that a dude doesn't breed with itself 
			b = randrange(0, len(population))
		child = create_ann()
		child.combine_weights(population[a].weights, population[b].weights)
		children.append(child)
		if(random() < mutation_rate):
			child.mutate_weights(1)
		children[i].fit()
	return children

if __name__ == "__main__":

	seed()
	population = []
	breeding_population = []
	population_size = 750
	number_of_iterations = 40
	mutation_rate = .1
	selection_rate = .2  # selection is deterministic
	input_vector = [0, 1, 0, 0]

	if(len(argv)>4):
		selection_rate = float(argv[4])
	if(len(argv)>3):
		mutation_rate = float(argv[3])
	if(len(argv)>2):
		number_of_iterations = int(argv[2])
	if(len(argv)>1):
		population_size = int(argv[1])

	# generate initial population
	for i in range(0, population_size):
		population.append(create_ann())
		population[i].fit()

	best = population[0]

	# begin generations
	for i in range(0, number_of_iterations):
		population.sort(key = lambda i: i.fitness)
		if best.fitness < population[len(population)-1].fitness:
			best = population[len(population)-1]
		population = population[int(len(population)*(1 - selection_rate)):]
		population = mate_population(population, population_size, mutation_rate)
		print("Best after " + str(i) + " iterations: " + str(best) + "\n")

	best_out = []
	best.evaluate(input_vector, best_out)
	print("----------------------------------------\n Final best:\noutput = " + str((best_out / (0xFFFFFFFF / 2)) - 1) + "\nfitness = " + str(best.fitness) )
