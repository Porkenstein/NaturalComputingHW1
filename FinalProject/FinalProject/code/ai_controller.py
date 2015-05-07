from game import *
from phase_ann2 import *

class AI:
	# decisions: pick role, pick building, pick plantation, pick trade crop, pick captain crop, prioritize crops to save, 
	#			 prioritize new workers, use hacienda, use hospice, use university, use wharf
	__init__(self, w_pick_role, w_pick_building, w_pick_plantation, w_pick_trade, w_pick_captain, w_prioritize_save, w_prioritize_workers, \
		w_use_hacienda, w_use_university, w_use_wharf):

		self.ann_pick_role = phase_ann( , )
		self.ann_pick_role.weights = w_pick_role

    	self.ann_pick_building = phase_ann ( , )
		self.ann_pick_building.weights = w_pick_building

		self.ann_pick_plantation = phase_ann ( , )
		self.ann_pick_plantation.weights = w_pick_plantation

		self.ann_pick_trade = phase_ann ( , )
		self.ann_pick_trade.weights = w_pick_trade

		self.ann_pick_captain = phase_ann ( , )
		self.ann_pick_captain.weights = w_pick_captain

		self.ann_prioritize_save = phase_ann ( , )
		self.ann_prioritize_save.weights = w_prioritize_save

		self.ann_prioritize_workers = phase_ann ( , )
		self.ann_prioritize_workers.weights = w_prioritize_workers

		self.ann_use_hacienda = phase_ann ( , )
		self.ann_use_hacienda.weights = w_use_hacienda

		self.ann_use_university = phase_ann ( , )
		self.ann_use_university.weights = w_use_university

		self.ann_use_wharf = phase_ann ( , )
		self.ann_use_wharf.weights = w_use_wharf
