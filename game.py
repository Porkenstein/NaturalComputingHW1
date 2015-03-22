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
	small_market = 1
	#...

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
		self.capacity = 12 #?
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
		print("Player " + str(player_num) + ": Pick a role number")
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
				if BID(temp) in player_roles and buildings[BID(temp)][1]>0: # if the building is available
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
		
		self.governor = 0 # 0th player starts first
		self.current_player = 0
		self.colonists_left = 100 #?
		self.trade_house = [Crop.none] * 4
		self.ships = [None]*(5)  # the last is for the player with the harbor #?
		self.plantations = []
		self.cities = [City()]*num_players
		self.ships[0] = Ship(5)
		self.ships[1] = Ship(6)
		self.ships[2] = Ship(7)
		self.ships[3] = Ship(8)
		self.ships[4] = Ship(7)

		self.store = \
									#building, amount available
			{ BID.small_market : [Building(1, 2, 1, "Small Market"), 3] \ #?
			{ BID.small_market : [Building(1, 2, 1, "Small Market"), 3] \
			#...
			}
		
		temp = []
		for i in range(0, 200): #?
			temp.append(Crop(i%5))
		shuffle(temp)			
		plantations = [temp[0:49], temp[50:99], temp[100:149], temp[150:200]]
		
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
