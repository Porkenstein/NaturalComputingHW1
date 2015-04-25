from math import *
from random import *
from sys import *
from enum import *

# a simulation of a 3-player game of puerto rico
#
# Some assumptions that we're making here:
# 1. The players are placing their buildings in an efficient manner, such that
#    the number of spaces left in their city is enough to determine placement availability
#
# 2. The players never run out of plantation spots

class Role(Enum):
	none = 0
	captain = 1
	trader = 2
	builder = 3
	settler = 4
	craftsman = 5
	mayor = 6

# building ID is used when applying modifiers
class BID(Enum):
	none = 0
	small_indigo_plant = 1
	small_sugar_mill = 2
	small_market = 3
	hacienda = 4
	construction_hut = 5
	small_warehouse = 6
	indigo_plant = 7
	sugar_mill = 8
	hospice = 9
	office = 10
	large_market = 11
	large_warehouse = 12
	tobacco_storage = 13
	coffee_roaster = 14
	factory = 15
	university = 16
	harbor = 17
	wharf = 18
	guild_hall = 19
	residence = 20
	fortress = 21
	customs_house = 22
	city_hall = 23

# the .value of the crop is equivalent to its base sale value
class Crop(Enum):
	none = -2
	quarry = -1
	corn = 0
	indigo = 1
	sugar = 2
	coffee = 3
	tobacco = 4

# lists of these are in the store and on each player's board
class Building:
	def __init__(self, size, cost, workers, name):
		self.size = size
		self.cost = cost
		self.workers = workers
		self.name = name

class Ship:
	def __init__(self, capacity):
		self.capacity = capacity
		self.crop = Crop.none
		self.cargo = 0

	# try to fill the ship with all of one crop, return what doesn't fit
	def fill(self, crop, amount):
		if self.crop == Crop.none:
			self.crop = crop
		self.cargo = min(self.capacity, self.cargo + amount)
		return max(0, self.cargo + amount - self.capacity)

	# depart, clearing all crops
	def depart(self):
		self.crop = Crop.none
		self.cargo = 0

class City:
	def __init__(self):
		self.capacity = 12
		self.used = 0
		self.buildings = []
	
	def add_building(self, building):
		if (self.capacity < self.used + building.size)
			return false
		self.buildings.append(building)
		self.used += building.size
		return true
	
class Console:
	def get_role(player_roles, player_num):
		print("Player " + str(player_num) + ": Pick a role number\n")
		for i in range(1, 6):
			if not Role(i) in player_roles:
				print(str(i) + ". " + str(Role(i)))
		# fish for input until input is valid
		While True:
			temp = input(str(player_num) + ">>")
			if temp.isdigit() and temp < 7 and temp > 0:
				temp = Role(int(temp))
				if not Role(temp) in player_roles:
					return temp

	def get_building(buildings, player_num):
		print("Player " + str(player_num) + ": Pick a building number")
		for i in range(1, 20) #?:
			if BID(i) in buildings and buildings[BID(i)][1]>0: # if the building is available
				print(str(i) + ". " + buildings[BID(i)][0].name)
		# fish for input until input is valid
		While True:
			temp = input(str(player_num) + ">>")
			if temp.isdigit() and temp < 20 and temp > 0: #?
				temp = BID(int(temp))
				if buildings(temp) in buildings and buildings[BID(temp)][1]>0: # if the building is available
					return temp

	def get_ship(ships, player_num):
		print("Player " + str(player_num) + ": Pick a ship number")
		for i in range(1, len(ships)) #?:
			print(str(i) + ". Crop: " + str(ships[i].crop) + " Cargo" + str(ships[i].cargo) + "/" + str(ships[i].capacity))
		# fish for input until input is valid
		While True:
			temp = input(str(player_num) + ">>")
			if temp.isdigit() and temp < len(ships) and temp > 0: #?
				return ships[temp]

	def get_crop(player_crops, ):
		print("Player " + str(player_num) + ": Pick a ship number")
		for i in range(1, len(ships)) #?:
			print(str(i) + ". Crop: " + str(ships[i].crop) + " Cargo" + str(ships[i].cargo) + "/" + str(ships[i].capacity))
		# fish for input until input is valid
		While True:
			temp = input(str(player_num) + ">>")
			if temp.isdigit() and temp < len(ships) and temp > 0: #?
				return ships[temp]

class Game:	
	def __init__(self, num_players):
		self.num_players = num_players
		self.roles[3] = [Role.none] * num_players
		self.gold[3] = [0] * num_players
		self.victory_points[3] = [0] * num_players
		
		self.governor = 0 # 0th player starts first
		self.current_player = 0
		self.colonists_left = 55 # for 3 players
		self.trade_house = [Crop.none] * 4
		self.ships = [None]*(5)  # ships[num players + 1] is for the player with the wharf
		self.plantations = []
		self.cities = [City()]*num_players
		self.available_roles = [ Role.trader, Role.builder, Role.settler, Role.craftsman, Role.mayor ] # add and remove roles as players select them

		self.ships[0] = Ship(4)
		self.ships[1] = Ship(5)
		self.ships[2] = Ship(6)
		self.ships[3] = Ship(7)
		self.ships[4] = Ship(8)

		self.store = \
									#[size, cost, workers, name], amount available, number of quarries which can be used to buy
			{ 
			  BID.small_indigo_plant : [Building(1, 1, 1, "Small Indigo Plant"), 4, 1] \
			  BID.small_market : [Building(1, 1, 1, "Small Market"), 2, 1] \
			  BID.small_sugar_mill : [Building(1, 2, 1, "Small Sugar Mill"), 4, 1] \
			  BID.hacienda : [Building(1, 2, 1, "Hacienda"), 2, 1] \
			  BID.construction_hut : [Building(1, 2, 1, "Construction Hut"), 2, 1] \
			  BID.small_warehouse : [Building(1, 3, 1, "Small Warehouse"), 2, 1] \
			  BID.indigo_plant : [Building(1, 3, 3, "Indigo Plant"), 3, 2] \
			  BID.sugar_mill : [Building(1, 4, 3, "Sugar Mill"), 3, 2] \
			  BID.hospice : [Building(1, 4, 1, "Hospice"), 2, 2] \
			  BID.office : [Building(1, 5, 1, "Office"), 2, 2] \
			  BID.large_market : [Building(1, 5, 1, "Large Market"), 2, 2] \
			  BID.large_warehouse : [Building(1, 6, 1, "Large Warehouse"), 2, 2] \
			  BID.tobacco_storage : [Building(1, 5, 3, "Tobacco Storage"), 3, 3] \
			  BID.coffee_roaster : [Building(1, 6, 2, "Coffee Roaster"), 3, 3] \
			  BID.factory : [Building(1, 7, 1, "Factory"), 2, 3] \
			  BID.university : [Building(1, 8, 1, "University"), 2, 3] \
			  BID.harbor : [Building(1, 8, 1, "Harbor"), 2, 3] \
			  BID.wharf : [Building(1, 9, 1, "Wharf"), 2, 3] \
			  BID.guild_hall : [Building(2, 10, 1, "Guild Hall"), 1, 4] \
			  BID.residence : [Building(2, 10, 1, "Residence"), 1, 4] \
			  BID.fortress : [Building(2, 10, 1, "Fortress"), 1, 4] \
			  BID.customs_house : [Building(2, 10, 1, "Customs House"), 1, 4] \
			  BID.city_hall : [Building(2, 10, 1, "City Hall"), 1, 4] \
			}
		
		temp = []
		for i in range(0, 200): #?
			temp.append(Crop(i%5))
		shuffle(temp)
		self.plantations = [temp[0:49], temp[50:99], temp[100:149], temp[150:200]]
		
	def game_turn(self):
		for i in range(0, num_players):
			
			end_game_turn()

	def end_game_turn(self):
		self.roles = [Role.none] * self.num_players
		self.governor = (self.governor + 1)%num_players
		self.current_player = self.governor
		
	def end_player_turn(self):
		if((self.governor == 0 and self.current == self.num_players -1) or self.current == self.governor - 1)
			self.end_game_Turn()
		else
			self.current_player = self.current + 1 % self.num_players
	
if __name__ == "__main__":
	num_players = 3	
	if(sys.argc > 1):
		num_players = sys.argv[1]
	game = Game(num_players)
	
	while game.colonists_left > 0:
		game.game_turn()
