from math import *
from random import random, shuffle, randint
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

	def __str__(self): # for pretty printing
		return self.__repr__()[self.__repr__().index('.')+1:self.__repr__().index(':')].title()

# because of strange issues I was having
RoleList = [ Role.none, Role.captain, Role.trader, Role.builder, Role.settler, Role.craftsman, Role.mayor ]

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

	def __str__(self):
		return self.__repr__()[self.__repr__().index('.')+1:self.__repr__().index(':')].title()

# because of that strange issue
CropList = [ Crop.corn, Crop.indigo, Crop.sugar, Crop.coffee, Crop.tobacco]

# lists of these are in the store and on each player's board
class Building:
	def __init__(self, size, cost, workers, name, bid, production = Crop.none):
		self.size = size
		self.cost = cost
		self.workers = workers
		self.name = name
		self.assigned = 0
		self.production = production
		self.bid = bid

	def new(self):
		return Building(self.size, self.cost, self.workers, self.name, self.bid, self.production)

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

	def is_full(self):
		return self.cargo == self.capacity

class City:
	# The san juan of each parallel universe
	def __init__(self):
		self.capacity = 12
		self.used = 0
		self.buildings = []
		self.unemployed = 0
		self.plantation = []
	
	def add_building(self, building):
		if (self.capacity < self.used + building.size):
			return false
		self.buildings.append(building)
		self.used += building.size
		return true

	def assign_worker(self, building_no):
		print(building_no)
		if int(building_no) < len(self.buildings):
			if self.buildings[building_no].assigned < self.buildings[building_no].workers and self.unemployed > 0:
				self.buildings[building_no].assigned += 1
				self.unemployed -= 1
		else:
			if not self.plantation[building_no - len(self.buildings)][1]:
				self.plantation[building_no - len(self.buildings)][1] = True
				self.unemployed -= 1
				print("filling " + str(self.plantation[building_no - len(self.buildings)][1]))

	def get_blank_spaces(self, buildings_only = False):
		blanks = 0
		for bld in self.buildings:
			blanks += (bld.workers - bld.assigned)
		for p in self.plantation:
			if (not p[1]) and (not buildings_only):
				blanks += 1
		return blanks
		
	
class Console:
	def get_role(self, player_roles, player_num, role_gold):
		print("Player " + str(player_num) + ": Pick a role number\n")
		for i in range(1, 7):
			if not Role(i) in player_roles:
				print(str(i) + ". " + str(Role(i)) + "(" + str(role_gold[i]) + " Doubloons)")
		# fish for input until input is valid
		while True:
			temp = input(str(player_num) + ">>")
			if temp.isdigit() and int(temp) < 7 and int(temp) > 0:
				temp = Role(int(temp))
				if not temp in player_roles:
					return temp


	def get_building(self, store, player_num, quarries):
		print("Player " + str(player_num) + ": Pick a store item")
		for i in range(1, 24):
			if BID(i) in store and store[BID(i)][1]>0: # if the building is available
				print(str(i) + ". " + store[BID(i)][0].name + " (" + str(store[BID(i)][1]) + " available, " + str(store[BID(i)][0].cost - min(store[BID(i)][2], quarries)) + " doubloons )")
		# fish for input until input is valid
		while True:
			temp = input(str(player_num) + ">>")
			if temp.isdigit() and int(temp) < 24 and int(temp) > 0: #?
				temp = BID(int(temp))
				if temp in store and store[temp][1]>0: # if the building is available
					return temp

	def get_ship(self, ships, player_num):
		print("Player " + str(player_num) + ": Pick a ship number")
		for i in range(1, len(ships)):
			print(str(i) + ". Crop: " + str(ships[i].crop) + " Cargo: " + str(ships[i].cargo) + "/" + str(ships[i].capacity))
		# fish for input until input is valid
		while True:
			temp = input(str(player_num) + ">>")
			if temp.isdigit() and int(temp) < len(ships) and int(temp) > 0: #?
				return ships[temp]

	def get_crop(self, crops, player_num):
		print("Player " + str(player_num) + ": Pick a crop number")
		for i in range(0, len(crops)):
			print(str(i) + ". " + str(crops[i]))
		# fish for input until input is valid
		while True:
			temp = input(str(player_num) + ">>")
			if temp.isdigit() and int(temp) < len(crops) and int(temp) >= 0 and crops[int(temp)] != Crop.none:
				return int(temp)

	def get_worker_space(self, city, player_num):
		print("Player " + str(player_num) + ": Pick a building number")
		for i in range(0, len(city.buildings)):
			if city.buildings[i].workers != city.buildings[i].assigned:
				print(str(i) + ". " + str(city.buildings[i].name + " (" + str(city.buildings[i].assigned)+ "/" + str(city.buildings[i].workers)+ " Workers)"))
		for i in range(0, len(city.plantation)):
			if not city.plantation[i][1]:
				print(str(i + len(city.buildings)) + ". " + str(city.plantation[i][0]) + " (0/1 Workers)") 
		# fish for input until input is valid
		while True:
			temp = input(str(player_num) + ">>")
			if temp.isdigit() and int(temp) < len(city.buildings) and (int(temp) >= 0) and (city.buildings[int(temp)].workers != city.buildings[int(temp)].assigned):
				return int(temp)
			elif temp.isdigit() and int(temp) >= len(city.buildings) and int(temp) < (len(city.buildings) + len(city.plantation)) and (not city.plantation[int(temp) - len(city.buildings)][1]):
				return int(temp)
			#print(city.buildings[i].workers != city.buildings[i].assigned)
			#print(int(temp) >= 0)
			#print(int(temp) < len(city.buildings))
		return -1
