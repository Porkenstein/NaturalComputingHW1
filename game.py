from game_objects import *

# a simulation of a 3-player game of puerto rico
#
# Some assumptions that we're making here:
# 1. The players are placing their buildings in an efficient manner, such that
#    the number of spaces left in their city is enough to determine placement availability
#
# 2. The players take turns arranging their colonists in the mayor phase

class Game:	
	def __init__(self, num_players):
		self.winner = None
		self.num_players = num_players
		self.roles = [Role.none] * num_players
		self.gold = [200] * num_players
		self.victory_points = [0] * num_players
		self.victory_points_max = 75
		self.console = Console()
		self.role_gold = [0] * 7
		
		self.governor = 0 # 0th player starts first
		self.current_player = 0
		self.colonists_left = 55 # for 3 players
		self.trade_house = [Crop.none] * 4
		self.ships = [None]*(5)  # ships[num players + 1] is for the player with the wharf
		self.plantations = []
		self.cities = [City()]*num_players
		self.available_roles = [ Role.trader, Role.builder, Role.settler, Role.craftsman, Role.mayor, Role.captain ] # add and remove roles as players select them

		self.ships[0] = Ship(4)
		self.ships[1] = Ship(5)
		self.ships[2] = Ship(6)
		self.ships[3] = Ship(7)
		self.ships[4] = Ship(8)

		self.store = \
			{ #[size, cost, workers, name], amount available, number of quarries which can be used to buy
			  BID.small_indigo_plant : [Building(1, 1, 1, "Small Indigo Plant"), 4, 1], \
			  BID.small_market : [Building(1, 1, 1, "Small Market"), 2, 1], \
			  BID.small_sugar_mill : [Building(1, 2, 1, "Small Sugar Mill"), 4, 1], \
			  BID.hacienda : [Building(1, 2, 1, "Hacienda"), 2, 1], \
			  BID.construction_hut : [Building(1, 2, 1, "Construction Hut"), 2, 1], \
			  BID.small_warehouse : [Building(1, 3, 1, "Small Warehouse"), 2, 1], \
			  BID.indigo_plant : [Building(1, 3, 3, "Indigo Plant"), 3, 2], \
			  BID.sugar_mill : [Building(1, 4, 3, "Sugar Mill"), 3, 2], \
			  BID.hospice : [Building(1, 4, 1, "Hospice"), 2, 2], \
			  BID.office : [Building(1, 5, 1, "Office"), 2, 2], \
			  BID.large_market : [Building(1, 5, 1, "Large Market"), 2, 2],\
			  BID.large_warehouse : [Building(1, 6, 1, "Large Warehouse"), 2, 2], \
			  BID.tobacco_storage : [Building(1, 5, 3, "Tobacco Storage"), 3, 3], \
			  BID.coffee_roaster : [Building(1, 6, 2, "Coffee Roaster"), 3, 3], \
			  BID.factory : [Building(1, 7, 1, "Factory"), 2, 3], \
			  BID.university : [Building(1, 8, 1, "University"), 2, 3], \
			  BID.harbor : [Building(1, 8, 1, "Harbor"), 2, 3], \
			  BID.wharf : [Building(1, 9, 1, "Wharf"), 2, 3], \
			  BID.guild_hall : [Building(2, 10, 1, "Guild Hall"), 1, 4], \
			  BID.residence : [Building(2, 10, 1, "Residence"), 1, 4], \
			  BID.fortress : [Building(2, 10, 1, "Fortress"), 1, 4], \
			  BID.customs_house : [Building(2, 10, 1, "Customs House"), 1, 4], \
			  BID.city_hall : [Building(2, 10, 1, "City Hall"), 1, 4] \
			}
		
		temp = []
		for i in range(0, 8):
			temp.append(Crop.coffee)
		for i in range(0, 9):
			temp.append(Crop.tobacco)
		for i in range(0, 10):
			temp.append(Crop.corn)
		for i in range(0, 11):
			temp.append(Crop.sugar)
		for i in range(0, 12):
			temp.append(Crop.indigo)
		shuffle(temp)
		self.plantation_deck = [temp[0:11], temp[12:24], temp[25:37], temp[38:50]]
		self.quarries_remaining = 8
		
	def role_turn(self, role):
		role_player = self.roles.index(role)
		currentplayer = role_player
		colonist_ship = max(3, self.cities[0].get_blank_spaces() + self.cities[1].get_blank_spaces() + self.cities[2].get_blank_spaces())

		while(True):
			if (role is Role.captain):
				self.captain_phase(currentplayer)
			elif (role is Role.trader):
				self.trader_phase(currentplayer)
			elif (role is Role.craftsman):
				self.craftsman_phase(currentplayer)
			elif (role is Role.builder):
				self.builder_phase(currentplayer)
			elif (role is Role.settler):
				self.settler_phase(currentplayer)
			elif (role is Role.mayor):	
				self.mayor_phase(currentplayer, colonist_ship)
			else:
				print("\nError: no role\n")
			currentplayer = (currentplayer + 1)%num_players
			if(currentplayer is role_player):
				return

	# Returns whether or not to end the game
	def game_end_contition(self):
		if ( self.roles[self.current_player] == Role.captain ) and (sum(self.victory_points) >= self.victory_points_max ):
			return true
		if ( self.colonists_left <= 0):
			return true
		if ( self.cities[0].used == self.cities[0].capacity or self.cities[1].used == self.cities[1].capacity or self.cities[2].used == self.cities[2].capacity):
			return true

	def end_game(self):
		self.winner = self.victory_points.index(max(self.victory_points))

	def end_game_turn(self):
		self.roles = [Role.none] * self.num_players
		self.governor = (self.governor + 1)%num_players
		self.current_player = self.governor
		
	# Returns whether or not to continue the game turn
	def end_player_turn(self):
		if self.game_end_contition():
			self.end_game()
		if(((self.governor == 0) and (self.current_player == (self.num_players -1))) or (self.current_player == (self.governor - 1))):
			self.end_game_turn()
			return False
		else:
			self.current_player = (self.current_player + 1) % self.num_players
			return True
		
	def game_turn(self):
		selector = self.governor
		self.roles[selector] = self.console.get_role(self.roles, selector, self.role_gold)
		self.gold[selector] += self.role_gold[RoleList.index(self.roles[selector])]
		self.role_gold[RoleList.index(self.roles[selector])] = 0;
		selector = (selector + 1) % 3
		while selector != self.governor:
			self.roles[selector] = self.console.get_role(self.roles, selector, self.role_gold)
			self.gold[selector] += self.role_gold[RoleList.index(self.roles[selector])]
			self.role_gold[RoleList.index(self.roles[selector])] = 0;			
			selector = (selector + 1) % 3

		# throw doubloons on all roles which were not chosen	
		for i in range(0, 7):
			if not (Role(i) in self.roles):
				self.role_gold[i] += 1		

		self.current_player = self.governor
		while True:
			# do the phase of the current player
			self.role_turn(self.roles[self.current_player])
			if ( not self.end_player_turn()):
				return

	def captain_phase(self, player):
		print("CAPTAIN PHASE")
		return

	def trader_phase(self, player):
		print("TRADER PHASE")
		return

	def craftsman_phase(self, player):
		print("CRAFTSMAN PHASE")
		return

	def builder_phase(self, player):
		print("BUILDER PHASE for player " + str(player))
		choice = self.console.get_building(self.store, player)
		while (self.gold[player] < (self.store[choice][0].cost - min(self.store[choice][2], self.plantations[player].count(Crop.quarry)))):
			print("Not enough doubloons.")
			choice = self.console.get_building(self.store, player)
		return
	
	def settler_phase(self, player):
		print("SETTLER PHASE")
		return

	def mayor_phase(self, player, colonist_ship):
		print("MAYOR PHASE for player " + str(player))
		take = colonist_ship // 3
		if self.roles[player] == Roles.mayor:
			take +=1
		for i in range(0, take):
			if self.cities[player].get_blank_spaces() == 0:
				self.cities[player].unemployed += (take - i)
				return
			choice = self.console.get_worker_space(self.cities[player], player)
			self.cities[player].unemployed += 1
			self.cities[player].assign_worker(choice)
		# now give them the opportunity to assign unemployed citizens
		print("Player " + str(player) + " assign unemployed citizens")
		take = self.cities[player].unemployed		
		for i in range(0, take):
			choice = self.console.get_worker_space(self.cities[player], player)
			self.cities[player].assign_worker(choice)
		return

if __name__ == "__main__":
	num_players = 3
	game = Game(num_players)
	
	while game.winner == None:
		game.game_turn()
