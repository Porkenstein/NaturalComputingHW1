from game_objects import *
# a simulation of a 3-player game of Andreas Seyfarth and Rio Grande Games' " Puerto Rico "
#
# Meant to be played with a board, where the user moves what the computer says is moved.
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
		self.ships = [None]*(3)  # ships[num players + 1] is for the player with the wharf
		self.cities = [City(), City(), City()]
		self.available_roles = [ Role.trader, Role.builder, Role.settler, Role.craftsman, Role.mayor, Role.captain ] # add and remove roles as players select them
		self.quarries = 8
		self.can_ship = [True, True, True]

		self.ships[0] = Ship(4)
		self.ships[1] = Ship(5)
		self.ships[2] = Ship(6)

		self.wharf_used = [0,0,0] # keep track if each player has used their wharf ship(s) yet each captain phase

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
				self.goods[i].append(3)
		


	def get_goods_list(self, player):	# return an expansion of the goods list
		return self.goods[player][0] * [Crop.corn] + self.goods[player][1] * [Crop.indigo] + self.goods[player][2] * [Crop.sugar] + \
							self.goods[player][3] * [Crop.coffee] + self.goods[player][4] * [Crop.tobacco]


	def bonus(self, player, bid): # returns the number of a specified building a play has being worked		
		return sum((b.bid == bid) and (b.assigned == b.workers) for b in self.cities[player].buildings)




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
			if (role != Role.captain and currentplayer is role_player) or (role == Role.captain and (not (True in self.can_ship))): # either one full turn or nobody can ship

				if (role == Role.mayor):			# put new colonists on the colonist ship
					self.colonist_ship = max(self.num_players, \
						self.cities[0].get_blank_spaces(True) + self.cities[1].get_blank_spaces(True) + self.cities[2].get_blank_spaces(True))
					self.colonists_left -= self.colonist_ship

				if (role == Role.settler):			# draw new plantations
					for i in range(0, len(self.plantation_deck)):
						if (self.plantation_deck[i][0] == Crop.none) and (len(self.plantation_deck[i]) > 1): # make sure it's been drawn and the stack isn't empty
							del self.plantation_deck[i][0]

				if (role == Role.captain):
					self.wharf_used = [0,0,0]
					for p in range(0, 3):			# each player gets rid of crops
						print("Pick a barrel to keep")
						goods_list = self.get_goods_list(p)
						keep = goods_list[self.console.get_crop(goods_list, p)]	#choose crops to keep

						# use warehouses
						warehouses = self.bonus(p, BID.small_warehouse) + self.bonus(p, BID.large_warehouse)
						if warehouses > 0:
							goods_list = list(set(goods_list))
							store = [0, 0, 0, 0, 0]
							for w in range(0, warehouses):
								print("Pick a type of good to store in a warehouse.")
								temp = goods_list[self.console.get_crop(goods_list, p)]
								store[CropList.index(temp)] = self.goods[p][CropList.index(temp)] # note the amount of this crop to save
							self.goods[p] = store
							if store[CropList.index(keep)] == 0: # the additional barrel to keep
								self.goods[p][CropList.index(keep)] += 1
						else:
							self.goods[p] = [0, 0, 0, 0, 0] # if the poor sap doesn't have a warehouse
							self.goods[p][CropList.index(keep)] += 1

													# full ships are sent home to Spain
					for s in self.ships:
						if s.is_full():
							s.depart()

				if (role == Role.trader) and (len(self.trade_house) == 4):
					self.trade_house = []			#empty the trade house
					print("Trade house full!")
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

		# apply the large building bonuses
		for p in range(0, 3):

			# customs house needs to be calculated first because of its dependency on victory point chips
			if self.bonus(p, BID.customs_house) > 0:
				vp = self.victory_points[p] // 4
				print("Player " + str(p) + " gains " + str(vp) + " victory points from the Customs House.")

			if self.bonus(p, BID.guild_hall) > 0:
				vp = sum((b.production != Crop.none) and (b.workers == 1) for b in self.cities[p].buildings)
				vp += 2 * sum((b.production != Crop.none) and (b.workers != 1) for b in self.cities[p].buildings)
				print("Player " + str(p) + " gains " + str(vp) + " victory points from the Guild Hall.")

			if self.bonus(p, BID.residence) > 0:
				vp = max(4, len(self.cities[p].plantation) - 5)
				print("Player " + str(p) + " gains " + str(vp) + " victory points from the Residence.")

			if self.bonus(p, BID.fortress) > 0:
				vp = self.cities[p].get_total_colonists() // 3
				print("Player " + str(p) + " gains " + str(vp) + " victory points from the Fortress.")

			if self.bonus(p, BID.city_hall) > 0:
				vp = sum(b.production == Crop.none for b in self.cities[p].buildings)
				print("Player " + str(p) + " gains " + str(vp) + " victory points from the City Hall.")

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
		print("\nCAPTAIN PHASE for player " + str(player))
		# firstly, can the player actually ship anything? Build a crop list
		self.can_ship[player] = False
		goods_list = self.get_goods_list(player)
		crop_choices = []
		for s in self.ships:
			if s.crop == Crop.none:
				crop_choices += goods_list # we can ship whatever. purge doubles later
				self.can_ship[player] = True
				continue
			if s.crop in goods_list and not s.is_full():
				crop_choices.append(s.crop)
				self.can_ship[player] = True
		
		# the player can always use an empty wharf ship
		num_wharfs = self.bonus(player, BID.wharf) - self.wharf_used[player]
		if num_wharfs > 0:
			self.can_ship[player] = True
			crop_choices += goods_list

		if not self.can_ship[player]:
			print("Can't ship anything!")
			return

		# pick a crop to trade
		crop_choices = list(set(crop_choices)) # purge good doubles here
		crop_choice = crop_choices[self.console.get_crop(crop_choices, player)]

		load_ship = None
		most_empty = None
		# determine which ship we need to load our goods on (or perhaps use a wharf ship...?)
		if (num_wharfs > 0) and self.console.get_wharf(player):
			self.wharf_used[player] += 1
			amount = self.goods[player][CropList.index(crop_choice)]
			load_ship = Ship(amount)	
		else:
			for s in self.ships:
				if s.crop == crop_choice and not s.is_full(): # we must load onto this ship!
					load_ship = s
					break
				if s.crop == Crop.none and (most_empty == None or s.capacity > most_empty.capacity):
					most_empty = s
			if load_ship == None:
				load_ship = most_empty

			# now load the crop
			amount = min(load_ship.capacity - load_ship.cargo, self.goods[player][CropList.index(crop_choice)])

		# move cargo from the windrose to the ship
		self.goods[player][CropList.index(crop_choice)] -= amount
		load_ship.cargo += amount
		load_ship.crop = crop_choice
		print("Loaded " + str(amount) + " " + str(crop_choice) + " barrels onto cargo ship of size " + str(load_ship.capacity) + ".")

		# move VPs from the pile to the player, taking into account harbor
		amount += self.bonus(player, BID.harbor)
		print("Gained " + str(amount) + " victory points.")
		self.victory_points[player] += amount
		self.victory_points_max -= amount
		return



	def trader_phase(self, player):
		if len(self.trade_house) == 4:
			return
		print("\nTRADER PHASE for player " + str(player))
		possible_sales = self.get_goods_list(player)
		
		# get rid of goods already in the trade house, if the player doesn't have an office
		if self.bonus(player, BID.office) == 0:
			for good in self.trade_house:
				while good in possible_sales:
					possible_sales.remove(good)

		# pick a good to trade
		if len(possible_sales) == 0:
			print("Cannot trade anything!")
		else:
			choice = self.console.get_crop(possible_sales, player, True)
			if choice == None:
				return
			add_amount = CropList.index(possible_sales[choice]) + self.bonus(player, BID.small_market) + self.bonus(player, BID.large_market)
			if self.roles[player] == Role.trader:
				add_amount += 1 # trader privellege!
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

		# factory owner gets doubloons! +0/1/2/3/5 per factory
		if self.bonus(player, BID.factory) > 0:
			cash = len(crop_options) - 1
			if len(crop_options) == 5:
				cash += 1
			cash *= self.bonus(player, BID.factory)
			print("Earned " + str(cash) + " doubloons from factories.")			

		# get an extra crop if the player is the craftsman
		if (self.roles[player] == Role.craftsman) and (len(crop_options) > 0):
			print("Extra production for the craftsman")
			extra = self.console.get_crop(crop_options, player)
			self.goods[player][extra] += 1
		return



	def builder_phase(self, player):
		print("\nBUILDER PHASE for player " + str(player) + ".  You have " + str(self.gold[player]) + " doubloons.")
		choice = self.console.get_building(self.store, player, self.cities[player].quarries(), self.roles[player] == Role.builder)
 
		while (self.gold[player] < (self.store[choice][0].cost - min(self.store[choice][2], self.cities[player].quarries()))) and \
			(self.cities[player].capacity - self.cities[player].used) >= self.store[choice][0].size: # validate cost and size
			print("Cannot build " + self.store[choice][0].name + ".")
			choice = self.console.get_building(self.store, player, self.cities[player].quarries(), self.roles[player] == Role.builder)

		new_building = self.store[choice][0].new()

		# use the university, if applicable
		if self.bonus(player, BID.university) and self.console.get_university(player):
			new_building.assigned += 1

		self.cities[player].buildings.append(new_building)
		self.store[choice][1] -= 1
		self.gold[player] -= self.store[choice][0].cost

		return



	def settler_phase(self, player):
		print("\nSETTLER PHASE for player " + str(player) + ". ")
		if len(self.cities[player].plantation) > 11:
			print("Not enough island space for new plantations")
			return

		use_hospice = False
		# wanna use a hospice?
		if self.bonus(player, BID.hospice) > 0 and self.console.get_hospice(player):
			use_hospice = True

		choices = [self.plantation_deck[0][0], self.plantation_deck[1][0], self.plantation_deck[2][0], self.plantation_deck[3][0]] # skim off the top of the plantation deck
		if (self.roles[player] == Role.settler or self.bonus(player, BID.construction_hut) > 0) and self.quarries > 0: 
			# the settler, or anyone with a construction hut, can build quarries
			choices.append(Crop.quarry)
		choice = self.console.get_crop(choices, player, True)
		if choice == None:
			return
		self.cities[player].plantation.append([choices[choice], use_hospice]) # boolean says whether it's assigned to or not
		if choices[choice] == Crop.quarry:
			self.quarries -= 1
		else:
			self.plantation_deck[choice][0] = Crop.none

		# wanna use a hacienda?
		if self.bonus(player, BID.hacienda) > 0 and choices[choice] != Crop.quarry:
			for i in range(0, self.console.get_haciendas(player, self.bonus(player, BID.hacienda))):
				if (len(self.plantation_deck[choice]) == 1) or (len(self.cities[player].plantation) == 12):
					return
				self.cities[player].plantation.append([self.plantation_deck[choice][i+1], False])
				print("Also grabbed a " + str(self.plantation_deck[choice][i+1]) + " plantation.")
				del self.plantation_deck[choice][i+1]
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
