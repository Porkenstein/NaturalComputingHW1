from math import *
from random import *
from sys import *
#from game import *
from phase_ann2 import *
import operator

# This file is used to generate the AI file through tournament selection
# and an evolutionary program.

def create_ann():
	return phase_ann(4, 4, 4, 7, 7)

def fit_ann(ann, input_vector = None):
	# if no input vector passed, make it random
	if input_vector == None:
		input_vector = [getrandbits(1), getrandbits(1), getrandbits(1), getrandbits(1)]
	ans = input_vector[0]*2 + input_vector[1] + input_vector[2]*2 + input_vector[3]
	a_out = [0]*7
	ann.evaluate(input_vector, a_out)
	ann.fitness = abs(a_out.index(max(a_out))-ans)/ans

# starts running tournament selection to improve the weight sets given
# sorts them by rank and returns them
def run_tournament_selection(anns, max_iterations, input_vector):
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

		competitors = [anns[a], anns[b], anns[c]]
		for j in competitors:
			fit_ann(j)
		max_index, max_value = max(enumerate(competitors), key=lambda p: p.fitness)
		wincounts[max_index] += 1
		anns[max_index].fitness = 0
		max_index_2, max_value_2 = max(enumerate(competitors), key=lambda p: p.fitness)
		runnerupcounts[max_index_2] += 1
		anns[max_index].fitness = max_value

	for k in range(0, len(anns)):
		anns[k].fitness = wincounts[k] + runnerupcounts[k]/max(runnerupcounts)


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
	return children

if __name__ == "__main__":

	seed()
	population = []
	breeding_population = []
	population_size = 500
	number_of_iterations = 40
	mutation_rate = .1
	selection_rate = .2  # selection is deterministic
	input_vector = [0, 1, 0, 0]
	tournament_rounds = 100

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
	
	run_tournament_selection(population, tournament_rounds, input_vector)
	best = population[0]

	# begin generations
	for i in range(0, number_of_iterations):
		population.sort(key = lambda i: i.fitness)
		if best.fitness < population[len(population)-1].fitness:
			best = population[len(population)-1]
		population = population[int(len(population)*(1 - selection_rate)):]
		population = mate_population(population, population_size, mutation_rate)
		run_tournament_selection(population, tournament_rounds, input_vector)
		print("Best fitness after " + str(i) + " iterations: " + str(best.fitness) + " out of a max possible of " + str(tournament_rounds + 1) + "\n")

	best_out = []
	best.evaluate(input_vector, best_out)
	print("----------------------------------------\n Final best:\weights = " + str(best_out) + "\nfitness = " + str(best.fitness) + " out of a max possible of " + str(tournament_rounds + 1) + "\n" )
