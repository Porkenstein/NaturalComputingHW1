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
	def __init__(self, size, cost, workers, name, production_building = False):
		self.size = size
		self.cost = cost
		self.workers = workers
		self.name = name
		self.assigned = 0
		self.production_building = production_building

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
		self.unemployed = 0
	
	def add_building(self, building):
		if (self.capacity < self.used + building.size):
			return false
		self.buildings.append(building)
		self.used += building.size
		return true

	def assign_worker(self, building_no):
		if self.buildings[building_no].assigned < self.buildings[building_no].workers and self.unemployed > 0:
			self.buildings[building_no].assigned += 1
			self.unemployed -= 1

	def get_blank_spaces(self):
		blanks = 0
		for bld in self.buildings:
			blanks += (bld.workers - bld.assigned)
		return blanks
		
	
class Console:
	def get_role(self, player_roles, player_num):
		print("Player " + str(player_num) + ": Pick a role number\n")
		for i in range(1, 7):
			if not Role(i) in player_roles:
				print(str(i) + ". " + str(Role(i)))
		# fish for input until input is valid
		while True:
			temp = input(str(player_num) + ">>")
			if temp.isdigit() and int(temp) < 7 and int(temp) > 0:
				temp = Role(int(temp))
				if not Role(temp) in player_roles:
					return temp

	def get_building(self, buildings, player_num):
		print("Player " + str(player_num) + ": Pick a building number")
		for i in range(1, 24):
			if BID(i) in buildings and buildings[BID(i)][1]>0: # if the building is available
				print(str(i) + ". " + buildings[BID(i)][0].name)
		# fish for input until input is valid
		while True:
			temp = input(str(player_num) + ">>")
			if temp.isdigit() and int(temp) < 20 and int(temp) > 0: #?
				temp = BID(int(temp))
				if buildings(temp) in buildings and buildings[BID(temp)][1]>0: # if the building is available
					return temp

	def get_ship(self, ships, player_num):
		print("Player " + str(player_num) + ": Pick a ship number")
		for i in range(1, len(ships)):
			print(str(i) + ". Crop: " + str(ships[i].crop) + " Cargo" + str(ships[i].cargo) + "/" + str(ships[i].capacity))
		# fish for input until input is valid
		while True:
			temp = input(str(player_num) + ">>")
			if temp.isdigit() and int(temp) < len(ships) and int(temp) > 0: #?
				return ships[temp]

	def get_crop(self, player_crops, crops):
		print("Player " + str(player_num) + ": Pick a crop number")
		for i in range(1, len(crops)):
			print(str(i) + ". " + str(crops[i]))
		# fish for input until input is valid
		while True:
			temp = input(str(player_num) + ">>")
			if temp.isdigit() and int(temp) < len(crops) and int(temp) > 0:
				return crops[temp]

	def get_worker_space(self, city, player_num):
		#todo
		return 0
		


