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
		print("Cargo ship of size " + str(self.capacity) + " with " + str(self.crop) + " aboard departing for the old world. ¡Buen viaje!")
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

	def get_blank_spaces(self, buildings_only = False):
		blanks = 0
		for bld in self.buildings:
			blanks += (bld.workers - bld.assigned)
		for p in self.plantation:
			if (not p[1]) and (not buildings_only):
				blanks += 1
		return blanks

	def quarries(self):
		return sum((p[0] == Crop.quarry) and p[1] for p in self.plantation)
	
	def get_total_colonists(self):
		return sum(p[1] for p in self.plantation) + sum(b.assigned for b in self.buildings) + self.unemployed
		
	
class Console:

	def __init__(self, num_humans, ai):
		self.num_humans = num_humans
		self.selector = Selector(ai)
		
	def get_input(self, player, decision, game_state, invalids = None):
		if player < self.num_humans:
			return input(str(player) + ">>")
		else:
			decision = self.selector.get_input(player, decision, invalids)
			print(str(player) + ">>" + str(decision))

	def get_role(self, player_roles, player_num, role_gold, game_state):
		print("Player " + str(player_num) + ": Pick a role number\n")
		for i in range(1, 7):
			if not Role(i) in player_roles:
				print(str(i) + ". " + str(Role(i)) + "(" + str(role_gold[i]) + " Doubloons)")
		# fish for input until input is valid
		while True:
			temp = self.get_input(player_num, 0, game_state, player_roles)
			if temp.isdigit() and int(temp) < 7 and int(temp) > 0:
				temp = Role(int(temp))
				if not temp in player_roles:
					return temp


	def get_building(self, store, player_num, quarries, builder_discount = False):
		print("Player " + str(player_num) + ": Pick a store item")
		for i in range(1, 24):
			if BID(i) in store and store[BID(i)][1]>0: # if the building is available
				print(str(i) + ". " + store[BID(i)][0].name + " (" + str(store[BID(i)][1]) + " available, " + str(max(0, store[BID(i)][0].cost - min(store[BID(i)][2], \
					quarries) - int(builder_discount) )) + " doubloons )")
		# fish for input until input is valid
		while True:
			temp = input(str(player_num) + ">>")
			if temp.isdigit() and int(temp) < 24 and int(temp) > 0: #?
				temp = BID(int(temp))
				if temp in store and store[temp][1]>0: # if the building is available
					return temp

	def get_crop(self, crops, player_num, can_pick_none = False):
		print("Player " + str(player_num) + ": Pick a crop number")
		for i in range(0, len(crops)):
			print(str(i) + ". " + str(crops[i]))
		if can_pick_none:
			print("(enter nothing to do nothing)")
		# fish for input until input is valid
		while True:
			temp = input(str(player_num) + ">>")
			if can_pick_none and temp == "":
				return None
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
			elif temp.isdigit() and int(temp) >= len(city.buildings) and int(temp) < (len(city.buildings) + len(city.plantation)) and (not city.plantation[int(temp) \
				- len(city.buildings)][1]):
				return int(temp)
		return -1

	def get_haciendas(self, player_num, haciendas):
		print("Player " + str(player_num) + ": How many hacienda to use?")
		temp = input(str(player_num) + ">>")
		while (not temp.isdigit()) or (int(temp) > haciendas):
			temp = input(str(player_num) + ">>")
		return int(temp)

	def get_hospice(self, player_num):
		print("Player " + str(player_num) + ": Use the hospice? y/n")
		temp = input(str(player_num) + ">>")
		while not (temp in ['y', 'n']):
			temp = input(str(player_num) + ">>")
		return temp == 'y'

	def get_university(self, player_num):
		print("Player " + str(player_num) + ": Use the university? y/n")
		temp = input(str(player_num) + ">>")
		while not (temp in ['y', 'n']):
			temp = input(str(player_num) + ">>")
		return temp == 'y'

	def get_wharf(self, player_num):
		print("Player " + str(player_num) + ": Use the wharf? y/n")
		temp = input(str(player_num) + ">>")
		while not (temp in ['y', 'n']):
			temp = input(str(player_num) + ">>")
		return temp == 'y'



class Selector:
	# the sort of console equivalent for the Neural Net

	def __init__(self, ai):
		self.ai = ai

	def get_input(self, player, decision, game_state, invalids):
		if decision == 0:
			return self.ai[player].pick_role(game_state, invalids)
		elif decision == 1:
			return self.ai[player].pick_building(game_state, invalids)
		elif decision == 2:
			return self.ai[player].pick_plantation(game_state, invalids)
		elif decision == 3:
			return self.ai[player].pick_trade(game_state, invalids)
		elif decision == 4:
			return self.ai[player].pick_captain(game_state, invalids)
		elif decision == 5:
			return self.ai[player].pick_save(game_state, invalids)
		elif decision == 6:
			return self.ai[player].pick_workers(game_state, invalids)
		elif decision == 7:
			return self.ai[player].use_hacienda(game_state)
		elif decision == 8:
			return self.ai[player].use_university(game_state)
		elif decision == 9:
			return self.ai[player].use_wharf(game_state)
