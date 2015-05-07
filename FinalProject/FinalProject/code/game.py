from game_objects import *
# a simulation of a 3-player game of Andreas Seyfarth and Rio Grande Games' " Puerto Rico "
#
# Some assumptions that we're making here:
#
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
		self.colonist_ship = self.num_players
		self.goods = []
		
		self.governor = 0 # 0th player starts first
		self.current_player = 0
		self.colonists_left = 55 # for 3 players, minus initial colonist ship
		self.trade_house = []
		self.ships = [None]*(5)  # ships[num players + 1] is for the player with the wharf
		self.cities = [City(), City(), City()]
		self.available_roles = [ Role.trader, Role.builder, Role.settler, Role.craftsman, Role.mayor, Role.captain ] # add and remove roles as players select them
		self.quarries = 8

		self.ships[0] = Ship(4)
		self.ships[1] = Ship(5)
		self.ships[2] = Ship(6)
		self.ships[3] = Ship(7)
		self.ships[4] = Ship(8)

		self.store = \
			{ #[size, cost, workers, name], amount available, number of quarries which can be used to buy
			  BID.small_indigo_plant : [Building(1, 1, 1, "Small Indigo Plant", BID.small_indigo_plant, Crop.indigo), 4, 1], \
			  BID.small_market : [Building(1, 1, 1, "Small Market", BID.small_market), 2, 1], \
			  BID.small_sugar_mill : [Building(1, 2, 1, "Small Sugar Mill", BID.small_sugar_mill, Crop.sugar), 4, 1], \
			  BID.hacienda : [Building(1, 2, 1, "Hacienda", BID.hacienda), 2, 1], \
			  BID.construction_hut : [Building(1, 2, 1, "Construction Hut", BID.construction_hut), 2, 1], \
			  BID.small_warehouse : [Building(1, 3, 1, "Small Warehouse", BID.small_warehouse), 2, 1], \
			  BID.indigo_plant : [Building(1, 3, 3, "Indigo Plant", BID.indigo_plant, Crop.indigo), 3, 2], \
			  BID.sugar_mill : [Building(1, 4, 3, "Sugar Mill", BID.sugar_mill, Crop.indigo), 3, 2], \
			  BID.hospice : [Building(1, 4, 1, "Hospice", BID.hospice), 2, 2], \
			  BID.office : [Building(1, 5, 1, "Office", BID.office), 2, 2], \
			  BID.large_market : [Building(1, 5, 1, "Large Market", BID.large_market), 2, 2],\
			  BID.large_warehouse : [Building(1, 6, 1, "Large Warehouse", BID.large_warehouse), 2, 2], \
			  BID.tobacco_storage : [Building(1, 5, 3, "Tobacco Storage", BID.tobacco_storage, Crop.tobacco), 3, 3], \
			  BID.coffee_roaster : [Building(1, 6, 2, "Coffee Roaster", BID.coffee_roaster, Crop.coffee), 3, 3], \
			  BID.factory : [Building(1, 7, 1, "Factory", BID.factory), 2, 3], \
			  BID.university : [Building(1, 8, 1, "University", BID.university), 2, 3], \
			  BID.harbor : [Building(1, 8, 1, "Harbor", BID.harbor), 2, 3], \
			  BID.wharf : [Building(1, 9, 1, "Wharf", BID.wharf), 2, 3], \
			  BID.guild_hall : [Building(2, 10, 1, "Guild Hall", BID.guild_hall), 1, 4], \
			  BID.residence : [Building(2, 10, 1, "Residence", BID.residence), 1, 4], \
			  BID.fortress : [Building(2, 10, 1, "Fortress", BID.fortress), 1, 4], \
			  BID.customs_house : [Building(2, 10, 1, "Customs House", BID.customs_house), 1, 4], \
			  BID.city_hall : [Building(2, 10, 1, "City Hall", BID.city_hall), 1, 4] \
			}
		# build the randomized plantation deck
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
		
		# give the players their initial plantations and create the goods list
		self.cities[0].plantation.append([Crop.indigo, False])
		self.cities[1].plantation.append([Crop.indigo, False])
		self.cities[2].plantation.append([Crop.corn, False])
		for i in range(0, self.num_players):
			self.goods.append([])
			for j in range(0, 5):
				self.goods[i].append(0)
		print(self.goods)
		


	def role_turn(self, role):
		role_player = self.roles.index(role)
		currentplayer = role_player

		# loop through each player's sub-turn
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
				self.mayor_phase(currentplayer, self.colonist_ship)
			else:
				print("\nError: no role\n") #this shouldn't happen!
			currentplayer = (currentplayer + 1)%num_players

			# if the game is ending
			if(currentplayer is role_player):

				if (role == Role.mayor):			# put new colonists on the colonist ship
					self.colonist_ship = max(self.num_players, \
						self.cities[0].get_blank_spaces(True) + self.cities[1].get_blank_spaces(True) + self.cities[2].get_blank_spaces(True))
					self.colonists_left -= self.colonist_ship

				if (role == Role.settler):			# draw new plantations
					for i in range(0, len(self.plantation_deck)):
						if self.plantation_deck[i][0] == Crop.none:
							del self.plantation_deck[i][0]

				if (role == Role.captain):
					for p in range(0, 3):			# each player gets rid of crops
						print("Player " + str(p) + " pick a crop to keep")
						keep = [self.goods[p].pop(self.console.get_crop(self.goods[p], p))]
						self.goods = keep
													# full ships are sent home to Portugal
					for s in self.ships:
						if s.is_full():
							s.depart()

				if (role == Role.trader) and (len(self.trade_house) == 4):
					self.trade_house = []			#empty the trade house
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
		self.winner = self.victory_points.index(max(self.victory_points)) # we have a winner!



	def end_game_turn(self):	# there's a new governor
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
		# do-while of role selection and role turns
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
		print("\nCAPTAIN PHASE")
		return



	def trader_phase(self, player):
		if len(self.trade_house) == 4:
			return
		print("\nTRADER PHASE for player " + str(player))
		possible_sales = self.goods[player][0] * [Crop.corn] + self.goods[player][1] * [Crop.indigo] + self.goods[player][2] * [Crop.sugar] + \
			self.goods[player][3] * [Crop.coffee] + self.goods[player][4] * [Crop.tobacco]
		
		# get rid of goods already in the trade house
		for good in self.trade_house:
			while good in possible_sales:
				possible_sales.remove(good)

		# pick a good to trade
		if len(possible_sales) == 0:
			print("Cannot trade anything!")
		else:
			choice = self.console.get_crop(possible_sales, player)
			add_amount = CropList.index(possible_sales[choice]) # the index should be equal to the doubloon value
			self.trade_house.append(possible_sales[choice])
			print("Traded the " + str(possible_sales[choice]) + " for " + str(add_amount) + " doubloons.")
			self.gold[player] += add_amount
			self.goods[player][CropList.index(possible_sales[choice])] -= 1 # take one from the goods pile
		return



	def craftsman_phase(self, player):
		print("\nCRAFTSMAN PHASE for player " + str(player))
		crop_options = []
		# let's take a look at what goods the player gets
		for i in range(0, len(self.goods[player])):
			gather_crop = Crop(i)
			gather_count = sum((p[0] == gather_crop) and p[1] for p in self.cities[player].plantation) # count crops grown
			production_count = 0
			if gather_crop == Crop.corn:
				production_count = 12
			else:
				for b in self.cities[player].buildings:	# count possible production of this crop
					if (b.production == gather_crop):
						production_count += b.assigned
						if (not gather_crop in crop_options) and (b.assigned > 0):	# for the craftsman player's extra crop
							crop_options.append(gather_crop)
			self.goods[player][i] += min([production_count, gather_count])
			if min([production_count, gather_count]) > 0:
				print("Added " + str(min([production_count, gather_count])) + " " + str(gather_crop))
		if (self.roles[player] == Role.craftsman) and (len(crop_options) > 0):
			print("Extra production for the craftsman")
			extra = self.console.get_crop(crop_options, player)
			self.goods[player][extra] += 1
		return



	def builder_phase(self, player):
		print("\nBUILDER PHASE for player " + str(player) + ".  You have " + str(self.gold[player]) + " doubloons.")
		choice = self.console.get_building(self.store, player, self.cities[player].plantation.count(Crop.quarry)) 
		while (self.gold[player] < (self.store[choice][0].cost - min(self.store[choice][2], self.cities[player].plantation.count([Crop.quarry, True])))) and \
			(self.cities[player].capacity - self.cities[player].used) >= self.store[choice][0].size: # validate cost and size
			print("Cannot build " + self.store[choice][0].name + ".")
			choice = self.console.get_building(self.store, player, self.cities[player].plantation.count([Crop.quarry, True]))
		self.cities[player].buildings.append(self.store[choice][0].new())
		self.store[choice][1] -= 1
		self.gold[player] -= self.store[choice][0].cost
		return



	def settler_phase(self, player):
		print("\nSETTLER PHASE for player " + str(player) + ". ")
		if len(self.cities[player].plantation) > 11:
			print("Not enough island space for new plantations")
			return
		choices = [self.plantation_deck[0][0], self.plantation_deck[1][0], self.plantation_deck[2][0], self.plantation_deck[3][0]] # skim off the top of the plantation deck
		if self.roles[player] == Role.settler and self.quarries > 0: # the settler player can build quarries
			choices.append(Crop.quarry)
		choice = self.console.get_crop(choices, player)
		self.cities[player].plantation.append([choices[choice], False]) # boolean says whether it's assigned to or not
		if choices[choice] == Crop.quarry:
			self.quarries -= 1
		else:
			self.plantation_deck[choice][0] = Crop.none
		return



	def mayor_phase(self, player, colonist_ship):
		# how many colonists to take from the ship
		take = colonist_ship // 3
		if self.roles[player] == Role.mayor:
			take +=1
		print("\nMAYOR PHASE for player " + str(player) + ". " + str(colonist_ship) + " colonists on the ship this round. You get " + str(take) + " of them.")

		# assign each new colonist to a chosen space		
		for i in range(0, take):
			if self.cities[player].get_blank_spaces() == 0: #quit if there are no more blank spots
				self.cities[player].unemployed += (take - i)
				return
			choice = self.console.get_worker_space(self.cities[player], player)
			self.cities[player].unemployed += 1 # because assign_worker decrements unemployed
			self.cities[player].assign_worker(choice)

		# now give them the opportunity to assign unemployed citizens
		if (self.cities[player].unemployed > 0):
			print("Player " + str(player) + " assign " + str(self.cities[player].unemployed) + " unemployed citizens")
		take = self.cities[player].unemployed
		for i in range(0, take):
			if self.cities[player].get_blank_spaces() == 0:
				return
			choice = self.console.get_worker_space(self.cities[player], player)
			self.cities[player].assign_worker(choice)
		return



if __name__ == "__main__":
	num_players = 3
	game = Game(num_players)
	
	while game.winner == None:
		game.game_turn()
