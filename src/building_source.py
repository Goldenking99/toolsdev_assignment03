import logging
import random
import os
from functools import partial
import math
import pymel.core as pmc
from pymel.core import *

class BuildingCreate(object):

	building_count = 0

	def __init__(self, width, length, height, type):
		self.width = width
		self.length = length
		self.height = height
		self.type = type
		BuildingCreate.building_count += 1
		self.building_name = "Building_" + str(self.building_count)
		self.x_div = 10
		self.y_div = 10
		self.z_div = 10

	def make_building(self):
		if(type == 0):
			polyCube(w = self.width, d = self.length, h = self.height, n = str(self.building_name))

		elif(type == 1):
			polyCube(w = self.width, d = self.length, h = self.height, n = str(building_name))

			for extrude in range(0, random.randrange(0, 3)):
				polyExtrudeFacet(str(self.building_name) + ".f[1]", kft = False, ls = (0.8, 0.8, 0))
				polyExtrudeFacet(str(self.building_name) + ".f[1]", kft = False, ltz = 30)

		else:
			polyCube(w = self.width, d = self.length, h = self.height, sx = self.x_div, sy = self.y_div, sz = self.z_div, n = str(self.building_name))

			sides = []

			for side in range(0, 8):
				if(side != 1 and side != 3):
					side_math_one = self.x_div * self.y_div * side
					side_math_two = self.x_div * self.y_div * (side+1)
					sides.append(str(self.building_name) + ".f[" + str(side_math_one) + ":" + str(side_math_two - 1) + "]")

			polyExtrudeFacet(sides[0], sides[1], sides[2], sides[3], sides[4], sides[5], kft = False, ls = (0.8, 0.8, 0))
			windows = ls(sl = True)
			polyExtrudeFacet(windows[1], windows[2], windows[3], kft = False, ltz = -0.2)
			select(self.building_name)

	def move_building(self, x, y, z):
		select(self.building_name)
		move(x, y, z)
		select(cl = True)