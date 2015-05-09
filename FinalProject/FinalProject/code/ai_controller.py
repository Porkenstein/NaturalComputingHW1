from game import *
from phase_ann2 import *

GAME_STATE_LENGTH = 52
# 
# Note - each value representing an unbound amount is scaled logarithmically, with a practical max determined beforehand
#
# wealth - 1
# has_ for each building - 24
# abundance_ for each crop - 5
# production_strength_ for each crop - 5
# plantation_amount_ for each crop and quarry - 6
# ship availability (to me, for each crop. stronger = more spots.  0 = not available) - 5
# colonists_left - 1
# in_trade_house for each crop - 5
# colonists - 1
# unemployed - 1

class AI:
	# decisions: pick role, pick building, pick plantation, pick trade crop, pick captain crop, prioritize crops to save, 
	#			 prioritize new workers, use hacienda, use university, use wharf
	def __init__(self, weights = None):

		self.fitness = 0 # for evolution
		if weights == None:
			self.init_weights_random()
			return

		self.ann_pick_role = phase_ann( 3, GAME_STATE_LENGTH, 6, 6)
		self.ann_pick_role.weights = weights[0]

		self.ann_pick_building = phase_ann( 3, GAME_STATE_LENGTH, 24, 24)
		self.ann_pick_building.weights = weights[1]

		self.ann_pick_plantation = phase_ann( 3, GAME_STATE_LENGTH, 6, 6)
		self.ann_pick_plantation.weights = weights[2]

		self.ann_pick_trade = phase_ann( 3, GAME_STATE_LENGTH, 5, 5)
		self.ann_pick_trade.weights = weights[3]

		self.ann_pick_captain = phase_ann( 3, GAME_STATE_LENGTH, 5, 5)
		self.ann_pick_captain.weights = weights[4]

		self.ann_pick_save = phase_ann( 3, GAME_STATE_LENGTH, 5, 5)
		self.ann_pick_save.weights = weights[5]

		self.ann_pick_workers = phase_ann( 3, GAME_STATE_LENGTH, 30, 30) #24 buildings plus six crop types
		self.ann_pick_workers.weights = weights[6]

		self.ann_use_hacienda = phase_ann( 3, GAME_STATE_LENGTH, 2, 2)
		self.ann_use_hacienda.weights = weights[7]

		self.ann_use_university = phase_ann( 3, GAME_STATE_LENGTH, 2, 2)
		self.ann_use_university.weights = weights[8]

		self.ann_use_wharf = phase_ann( 3, GAME_STATE_LENGTH, 2, 2)
		self.ann_use_wharf.weights = weights[9]
	
	# create random set of weights
	def init_weights_random(self):
		self.ann_pick_role = phase_ann( 3, GAME_STATE_LENGTH, 6, 6)
		self.ann_pick_building = phase_ann( 3, GAME_STATE_LENGTH, 24, 24)
		self.ann_pick_plantation = phase_ann( 3, GAME_STATE_LENGTH, 6, 6)
		self.ann_pick_trade = phase_ann( 3, GAME_STATE_LENGTH, 5, 5)
		self.ann_pick_captain = phase_ann( 3, GAME_STATE_LENGTH, 5, 5)
		self.ann_pick_save = phase_ann( 3, GAME_STATE_LENGTH, 5, 5)
		self.ann_pick_workers = phase_ann( 3, GAME_STATE_LENGTH, 30, 30) #24 buildings plus six crop types
		self.ann_use_hacienda = phase_ann( 3, GAME_STATE_LENGTH, 2, 2)
		self.ann_use_university = phase_ann( 3, GAME_STATE_LENGTH, 2, 2)
		self.ann_use_wharf = phase_ann( 3, GAME_STATE_LENGTH, 2, 2)
		
	def pick_role(self, game_state, invalids):
		out = [0] * 6
		self.ann_pick_role.evaluate(game_state, out)
		out = [i[0] for i in sorted(enumerate(out), key=lambda x:x[1])]
		print(str(out) + " ROLE OUT")
		for i in invalids:
			out.remove(i)
		print(str(out) + " ROLE OUT PRUNED")		
		return out[0] + 1
	
	def pick_building(self, game_state, invalids):
		out = [0] * 24
		self.ann_pick_building.evaluate(game_state, out)
		out = [i[0] for i in sorted(enumerate(out), key=lambda x:x[1])]
		print(str(out) + " BUILDING OUT")
		for i in invalids:
			if i in out:
				out.remove(i)
		print(str(out) + " PRUNED BUILDING OUT")
		return out[0]

	def pick_plantation(self, game_state, invalids):
		out = [0] * 6
		self.ann_pick_plantation.evaluate(game_state, out)
		out = [i[0] for i in sorted(enumerate(out), key=lambda x:x[1])]
		for i in invalids:
			if i > -2:
				out.remove(i + 1)
		return out[0]

	def pick_trade(self, game_state, invalids):
		out = [0] * 6
		self.ann_pick_trade.evaluate(game_state, out)
		out = [i[0] for i in sorted(enumerate(out), key=lambda x:x[1])]
		print(str(out) + " TRADE OUT")
		for i in invalids:
			out.remove(i + 1)
		print(str(out) + " TRADE OUT PRUNED")
		return out[0]

	def pick_captain(self, game_state, invalids):
		out = [0] * 5
		self.ann_pick_captain.evaluate(game_state, out)
		out = [i[0] for i in sorted(enumerate(out), key=lambda x:x[1])]
		print(str(out) + " CAPTAIN OUT")
		print(str(invalids) + " CAPTAIN INVALIDS")
		for i in invalids:
			if i in out:
				out.remove(i)
		print(str(out) + " CAPTAIN OUT PRUNED")
		return out[0]

	def pick_save(self, game_state, invalids):
		out = [0] * 5
		self.ann_pick_save.evaluate(game_state, out)
		out = [i[0] for i in sorted(enumerate(out), key=lambda x:x[1])]
		for i in invalids:
			out.remove(i + 1)
		return out[0]

	def pick_workers(self, game_state, invalids):
		out = [0] * 30
		self.ann_pick_workers.evaluate(game_state, out)
		out = [i[0] for i in sorted(enumerate(out), key=lambda x:x[1])]
		print(str(out) + " WORKER OUT")
		print(str(invalids) + " WORKER INVALIDS")
		for i in invalids:
			out.remove(i)
		print(str(out) + " WORKER OUT PRUNED")
		return out[0]

	def use_hacienda(self, game_state):
		out = [0] * 2
		self.ann_use_hacienda.evaluate(game_state, out)
		if out.index(max(out)) == 0:
			return 'y'
		return 'n'

	def use_university(self, game_state):
		out = [0] * 2
		self.ann_use_university.evaluate(game_state, out)
		if out.index(max(out)) == 0:
			return 'y'
		return 'n'

	def use_wharf(self, game_state):
		out = [0] * 2
		self.ann_use_wharf.evaluate(game_state, out)
		if out.index(max(out)) == 0:
			return 'y'
		return 'n'
		
	def save_weights(self, filename):
		weights = [self.ann_pick_role.weights, self.ann_pick_building.weights, self.ann_pick_plantation.weights, self.ann_pick_trade.weights,\
		self.ann_pick_captain.weights, self.ann_pick_save.weights, self.ann_pick_workers.weights, self.ann_use_hacienda.weights,\
		self.ann_use_university.weights, self.ann_use_university.weights]
		
		pickle.dump( weights, open(filename,'wb'))
