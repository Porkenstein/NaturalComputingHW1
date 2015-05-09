from math import *
from random import *
from sys import *
from ai_controller import *
import operator
import os

# This file is used to generate the AI file through tournament selection
# and an evolutionary program.

def create_ann():
	return ai_controller()

def fit_ann(ann, input_vector, printy):
	# if no input vector passed, make it random
	#if input_vector == None:
	#	input_vector = [getrandbits(1), getrandbits(1), getrandbits(1), getrandbits(1)]
	#ans = input_vector[0]*2 + input_vector[1] + input_vector[2]*2 + input_vector[3]
	a_out = [0]*7
	ann.evaluate(input_vector, a_out)
	#if printy:
	#	print("\n||" + str(a_out) + "||\n")
	#if ans is 0:
	#	ann.fitness = abs(1 - abs((a_out.index(max(a_out))+1)-(ans+1))/(abs(a_out.index(max(a_out)) + (ans+1))))
	#else:
	#	ann.fitness = abs(1 - abs(a_out.index(max(a_out))-ans)/(abs(a_out.index(max(a_out)) + ans)))
	#print("\nfitness: " + str(ann.fitness) + " ans = "  + str(ans) + " guess = " + str(abs(a_out.index(max(a_out)))))
	return a_out.index(max(a_out))

def run_selection(anns):
	for ann in anns:
		ann.fitness = 0
		ann.fitness += int(fit_ann(ann, [0, 0, 0, 0], False) == 0)
		ann.fitness += int(fit_ann(ann, [0, 0, 0, 1], False) == 1)
		ann.fitness += int(fit_ann(ann, [0, 0, 1, 0], False) == 2)
		ann.fitness += int(fit_ann(ann, [0, 0, 1, 1], False) == 3)

		ann.fitness += int(fit_ann(ann, [0, 1, 0, 0], False) == 1)
		ann.fitness += int(fit_ann(ann, [0, 1, 0, 1], False) == 2)
		ann.fitness += int(fit_ann(ann, [0, 1, 1, 0], False) == 3)
		ann.fitness += int(fit_ann(ann, [0, 1, 1, 1], False) == 4)

		ann.fitness += int(fit_ann(ann, [1, 0, 0, 0], False) == 2)
		ann.fitness += int(fit_ann(ann, [1, 0, 0, 1], False) == 3)
		ann.fitness += int(fit_ann(ann, [1, 0, 1, 0], False) == 4)
		ann.fitness += int(fit_ann(ann, [1, 0, 1, 1], False) == 5)

		ann.fitness += int(fit_ann(ann, [1, 1, 0, 0], False) == 3)
		ann.fitness += int(fit_ann(ann, [1, 1, 0, 1], False) == 4)
		ann.fitness += int(fit_ann(ann, [1, 1, 1, 0], False) == 5)
		ann.fitness += int(fit_ann(ann, [1, 1, 1, 1], False) == 6)
		

# starts running random tournament selection.  the fitness of each ann (AI) is
# set equal to an amount reflectant to how many games they've won
def run_tournament_selection(anns, max_iterations):
	#done = []
	#used = [0] * len(anns)
	#max_used = (max_iterations // len(anns)) + 1
	wincounts = [0] * len(anns)
	runnerupcounts = [0] * len(anns) # use for tie breaking
	competitor_indecies = [0, 0, 0]
	for i in range(0, max_iterations):
		# select three random anns
		# run a single 3-AI game and get the winner and runner-up.  increment the values in the wincount and runnerupcount arrays
		for k in range(0,3):
			competitor_indecies[k] = randrange(0, len(anns))
		while competitor_indecies[0] == competitor_indecies[1] or competitor_indecies[0] == competitor_indecies[2] or competitor_indecies[1] == competitor_indecies[2]:
			for m in range(0,3):
				competitor_indecies[m] = randrange(0, len(anns))

		competitors = [anns[competitor_indecies[0]], anns[competitor_indecies[1]], anns[competitor_indecies[2]]]
		# run a 3-ai game
		game = Game(3, 0, competitors)
		while game.winner == None:
			game.game_turn()

		winner = competitor_indecies[game.winner]
		runnerup = competitor_indecies[game.runnerup]

		wincounts[winner] += 1
		runnerupcounts[runnerup] += 1

		
		# make sure that we don't overdo the number of wins 
		#for i in competitor_indecies:		
		#	used[i] += 1
		#	if used[i] == max_used:
		#		done.append(anns.pop(i))

	# put the removed AIs back
	#for d in done:
	#	anns.append(d)

	for k in range(0, len(anns)):
		anns[k].fitness = wincounts[k] + runnerupcounts[k]/float(max(runnerupcounts))


# fills a new population with mates, fits, mutates and returns it
def mate_population(population, n, mutation_rate):
	children = []
	for i in range(0, n):
		a = randrange(0, len(population))
		b = randrange(0, len(population))		
		while a == b:  # make sure that a dude doesn't breed with itself 
			b = randrange(0, len(population))
		child = create_ann()
		child.combine_weights(population[a], population[b])
		if(random.random() < mutation_rate):
			child.mutate_weights(1)
		children.append(child)
	return children

if __name__ == "__main__":

	f = open(os.devnull, 'w')
	sys.stdout = f

	seed()
	population = []
	breeding_population = []
	keep_ranks = 2
	population_size = 200
	number_of_iterations = 2000
	mutation_rate = .5
	selection_rate = .1  # selection is deterministic
	tournament_rounds = 200

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
	
	run_tournament_selection(population, tournament_rounds)
	best = population[0]

	# begin generations
	for i in range(0, number_of_iterations):

		# get the top fitnesses
		max_index, max_value = max(enumerate(population), key=lambda p: p[1].fitness)
		if(population[max_index].fitness > best.fitness):
			best = population[max_index]

		keep = [0] * keep_ranks
		for p in population:
			for k in range(0, keep_ranks):
				if keep[k] < p.fitness and not (p.fitness in keep):
					keep[k] = p.fitness

		# weed out the shitty fits
		for j in range(0, len(population)):
			if j >= len(population):
				break
			if not (population[j].fitness in keep):
				del population[j]
			
		print("New population size: " + str(len(population)))
			
		new_population = mate_population(population, population_size - len(population), mutation_rate)
		population = population + new_population
		run_touranment_selection(population, tournament_rounds)
		print("Best fitness after " + str(i) + " iterations: " + str(best.fitness) + " out of a max possible of 15\n")

	print("----------------------------------------\n Final best:  \nfitness = " + str(best.fitness)+ "\n" )
	print("Enter filename for AI " + str(i))
	filename = input(">>")	
	pickle.dump( weights, open(filename,'wb'))
