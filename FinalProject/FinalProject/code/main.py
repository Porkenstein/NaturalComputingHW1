from ai_controller import *



#  This is the main which should be run for the
#  Puerto Rico AI
if __name__ == "__main__":
	print("Puerto Rico - a game by Andreas Seyfarth.  Simulation by Derek Stotz and Chris Smith")
	print("------------------------------------------------------------------------------------\n")

	weights = []
	ai = []

	# ask for number of human players (0 - 3)
	print("How many human players?")
	num_players = input(">>")
	while (not num_players.isinteger()) or (int(num_players) > 3) or (int(num_players) < 0):
		num_players = input(">>")
	num_players = int(num_players) 

	# load weights from file
	for i in range(0, 3 - num_players):
		print("Enter filename for AI " + str(i))	
		weights.append(pickle.load(input(">>")))

		# create the AIs
		ai.append(AI(weights[i][0], weights[i][1], weights[i][2], weights[i][3], weights[i][4], weights[i][5], weights[i][6], weights[i][7], weights[i][8], weights[i][9]))

	# begin the game
	game = Game(3, num_players, weights)
	
	while game.winner == None:
		game.game_turn()
