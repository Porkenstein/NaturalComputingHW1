from math import *
from random import *
from sys import *
from enum import *

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

