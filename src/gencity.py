import logging
import random
import os
from functools import partial
import math
import pymel.core as pmc
from pymel.core import *

import building_source

class GenCity(object):
	"""This class is the main class in the city generation script. It accepts inputs from the GUI and implements them into the script. 
		The code also pulls from another class, building source, to create each individual building and then attaches it to it's list, building_list. 
		The generation script manipulates this list to go across the grid defined without stepping outside of the grid."""

	def __init__(self, length=100, width=100, max_height=70, block=125, gap=2, street=16):
		"""Inputs from user defined in GUI. If no input, then supplies default values"""
		self.length = length
		self.width = width
		self.max_height = max_height
		self.block = block
		self.gap = gap
		self.street = street

	def city_generator(self):
		"""Global variables needed for the script"""
		building_list = []

		building_base_x = 20
		building_base_z = 20
		building_min_width = 5
		building_min_height = 5

		x_space = 0
		x_space_max = 0
		counter = 0
		xcounter = 0

		group_building = group(em = True, n = "group_building")
		group_street = group(em = True, n = "street")

		"""Creates inital grid for building_list to scroll across"""
		polyPlane(w = self.width, h = self.length, n = "ground")
		move(self.width / 2, 0, self.length / 2)

		"""Logic to go across grid"""
		while(x_space < self.length):
			z_space = 0

			while(z_space < self.width):
				"""Establishes building limits inside the plot on the grid"""
				current_height = random.randrange(building_min_height, self.max_height)
				if(random.randrange(0, 100) > 90):
					current_height = current_height + (current_height * 0.7)
				building_z = random.randrange(building_min_width, building_base_z)
				building_x = random.randrange(building_min_width, building_base_x)

				if(building_x > x_space_max):
					x_space_max = building_x

				for z in range(z_space - 1, z_space + building_z + self.gap + 1):
					if(z % self.block == 0):
						street_segment = polyPlane(h = self.street, w = x_space_max + self.gap, sx = 1, sy = 1)
						move(x_space + (x_space_max / 2), 0.01, z + (self.street / 2))
						parent(street_segment[0], group_street)
						z_space = z + self.street + self.gap
						break
				"""Chooses a random building from 3 types, then adds those buildings to the list to be created"""
				building_type = random.randrange(0, 3)

				building = building_source.BuildingCreate(building_x, building_z, current_height, building_type)

				building_list.append(building)
				building_list[counter].make_building()
				parent(building_list[counter].building_name, group_building)

				"""Moves building into boundaries defined for it's block on the grid"""
				building_list[counter].move_building((x_space + (building_x / 2)), (current_height / 2), (z_space + (building_z / 2)))

				z_space = z_space + building_z + self.gap

				counter += 1

			"""Logic that dictates the streets surrounding the buildings"""
			if xcounter == 1:
				street_segment = polyPlane(h = self.width, w = self.street + self.gap, sx = 1, sy = 1)
				move(x_space + (self.street / 2) + x_space_max + self.gap, 0.01, self.width / 2)
				parent(street_segment[0], group_street)

				x_space = x_space + self.street + x_space_max + (self.gap * 2)
				xcounter = 0

			else:
				xcounter += 1
				
				x_space = x_space + x_space_max + self.gap

		streets = listRelatives(group_street, c = True)
		select(streets)
		polyUnite(n = "Combined_Street")
		delete(ch = True)