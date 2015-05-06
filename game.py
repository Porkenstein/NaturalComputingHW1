from math import *
from random import *
from sys import *
from enum import *
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
		self.available_roles = [ Role.trader, Role.builder, Role.settler, Role.craftsman, Role.mayor, Role.captain ] # add and remove roles as players select them

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
		
	def role_turn(self, role):
		role_player = self.roles.index(role)
		currentplayer = role_player

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
				self.mayor_phase(currentplayer)
			else
				print("\nError: no role\n")
			currentplayer = (currentplayer + 1)%num_players
			if(currentplayer is role_player):
				return

	
	def end_game_turn(self):
		self.roles = [Role.none] * self.num_players
		self.governor = (self.governor + 1)%num_players
		self.current_player = self.governor
		
	# Returns whether or not to continue the game turn
	def end_player_turn(self):
		if((self.governor == 0 and self.current == self.num_players -1) or self.current == self.governor - 1)
			self.end_game_Turn()
			return True
		else
			self.current_player = self.current + 1 % self.num_players
			return False
		
	def game_turn(self):
			selector = self.governor
		for i in range(0, self.num_players):
			# have the players select a role		
		
		while True:
			# do the phase of the current player
			self.role_turn(self.roles[])
			if (!self.end_player_turn())
				return;
	

if __name__ == "__main__":
	num_players = 3	
	if(sys.argc > 1):
		num_players = sys.argv[1]
	game = Game(num_players)
	
	while game.colonists_left > 0:
		game.game_turn()
