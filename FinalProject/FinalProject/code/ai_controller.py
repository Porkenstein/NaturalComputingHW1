from game import *
from phase_ann2 import *

GAME_STATE_LENGTH = 53
# 
# Note - each value representing an unbound amount is scaled logarithmically, with a practical max determined beforehand
#
# wealth - 1
# has_ for each building - 23
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
	#			 prioritize new workers, use hacienda, use hospice, use university, use wharf
	__init__(self, w_pick_role, w_pick_building, w_pick_plantation, w_pick_trade, w_pick_captain, w_pick_save, w_pick_workers, \
		w_use_hacienda, w_use_university, w_use_wharf):

		self.ann_pick_role = phase_ann( 3, GAME_STATE_LENGTH, 6, 6)
		self.ann_pick_role.weights = w_pick_role

    	self.ann_pick_building = phase_ann ( 3, GAME_STATE_LENGTH, 23, 23)
		self.ann_pick_building.weights = w_pick_building

		self.ann_pick_plantation = phase_ann ( 3, GAME_STATE_LENGTH, 6)
		self.ann_pick_plantation.weights = w_pick_plantation

		self.ann_pick_trade = phase_ann ( 3, GAME_STATE_LENGTH, 5)
		self.ann_pick_trade.weights = w_pick_trade

		self.ann_pick_captain = phase_ann ( 3, GAME_STATE_LENGTH, 5)
		self.ann_pick_captain.weights = w_pick_captain

		self.ann_pick_save = phase_ann ( 3, GAME_STATE_LENGTH, 5)
		self.ann_pick_save.weights = w_pick_save

		self.ann_pick_workers = phase_ann ( 3, GAME_STATE_LENGTH, 23, 23)
		self.ann_pick_workers.weights = w_pick_workers

		self.ann_use_hacienda = phase_ann ( 3, GAME_STATE_LENGTH, 2, 2)
		self.ann_use_hacienda.weights = w_use_hacienda

		self.ann_use_university = phase_ann ( 3, GAME_STATE_LENGTH, 2, 2)
		self.ann_use_university.weights = w_use_university

		self.ann_use_wharf = phase_ann ( 3, GAME_STATE_LENGTH, 2, 2)
		self.ann_use_wharf.weights = w_use_wharf
