import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance

import gencity
import savescene

def maya_main_window():
	"""Return the maya main window widget"""
	main_window = omui.MQtUtil.mainWindow()
	return wrapInstance(long(main_window), QtWidgets.QWidget)

class UserUI(QtWidgets.QDialog):
	""" Smart Save UI class """

	def __init__(self):
		"""Constructor"""
		# Passing the object UserUI as an argument to super()
		# makes this line python 2 and 3 compatible
		super(UserUI, self).__init__(parent=maya_main_window())
		self.scene = gencity.GenCity()
		self.scene_save = savescene.SceneFile()

		self.setWindowTitle("Procedural City Generator")
		self.resize(700,300)
		self.setWindowFlags(self.windowFlags() ^
							QtCore.Qt.WindowContextHelpButtonHint)
		self.create_widgets()
		self.create_layout()
		self.create_connections()

	def create_widgets(self):
		"""Create widgets for our UI"""

		"""Screen Title"""
		self.title_lbl = QtWidgets.QLabel("Procedural City Generator")
		self.title_lbl.setStyleSheet("font: bold 40px")

		"""City Height"""
		self.height_lbl = QtWidgets.QLabel("City Height")
		self.height_spinbox = QtWidgets.QSpinBox()
		self.height_spinbox.setRange(0,1000)
		self.height_spinbox.setValue(self.scene.max_height)

		"""City Length"""
		self.length_lbl = QtWidgets.QLabel("City Length")
		self.length_spinbox = QtWidgets.QSpinBox()
		self.length_spinbox.setRange(0,1000)
		self.length_spinbox.setValue(self.scene.length)

		"""City Width"""
		self.width_lbl = QtWidgets.QLabel("City Width")
		self.width_spinbox = QtWidgets.QSpinBox()
		self.width_spinbox.setRange(0,1000)
		self.width_spinbox.setValue(self.scene.width)

		"""Street Width"""
		self.street_lbl = QtWidgets.QLabel("Street Width")
		self.street_spinbox = QtWidgets.QSpinBox()
		self.street_spinbox.setRange(0,1000)
		self.street_spinbox.setValue(self.scene.street)

		"""City Block Size"""
		self.block_lbl = QtWidgets.QLabel("City Block Size")
		self.block_spinbox = QtWidgets.QSpinBox()
		self.block_spinbox.setRange(0,1000)
		self.block_spinbox.setValue(self.scene.block)

		"""Building Gap"""
		self.gap_lbl = QtWidgets.QLabel("Building Gap")
		self.gap_spinbox = QtWidgets.QSpinBox()
		self.gap_spinbox.setRange(0,1000)
		self.gap_spinbox.setValue(self.scene.gap)

		"""Buttons"""
		self.gen_btn = QtWidgets.QPushButton("Generate")
		self.cancel_btn = QtWidgets.QPushButton("Cancel")
		self.save_btn = QtWidgets.QCheckBox("Save")

	def create_layout(self):
		"""Lay out our widgets in the UI"""

		"""City Length Layout"""
		self.length_lay = QtWidgets.QHBoxLayout()
		self.length_lay.addWidget(self.length_lbl)
		self.length_lay.addWidget(self.length_spinbox)

		"""City Width Layout"""
		self.width_lay = QtWidgets.QHBoxLayout()
		self.width_lay.addWidget(self.width_lbl)
		self.width_lay.addWidget(self.width_spinbox)

		"""City Height Layout"""
		self.height_lay = QtWidgets.QHBoxLayout()
		self.height_lay.addWidget(self.height_lbl)
		self.height_lay.addWidget(self.height_spinbox)

		"""Building Gap Layout"""
		self.gap_lay = QtWidgets.QHBoxLayout()
		self.gap_lay.addWidget(self.gap_lbl)
		self.gap_lay.addWidget(self.gap_spinbox)

		"""City Block Layout"""
		self.block_lay = QtWidgets.QHBoxLayout()
		self.block_lay.addWidget(self.block_lbl)
		self.block_lay.addWidget(self.block_spinbox)

		"""Street Width Layout"""
		self.street_lay = QtWidgets.QHBoxLayout()
		self.street_lay.addWidget(self.street_lbl)
		self.street_lay.addWidget(self.street_spinbox)

		"""Bottom Button Layout"""
		self.bottom_btn_lay = QtWidgets.QHBoxLayout()
		self.bottom_btn_lay.addWidget(self.save_btn)
		self.bottom_btn_lay.addWidget(self.gen_btn)
		self.bottom_btn_lay.addWidget(self.cancel_btn)

		"""Main layout (Window elements arrangement should adhere to this order"""
		self.main_layout = QtWidgets.QVBoxLayout()
		self.main_layout.addWidget(self.title_lbl)
		self.main_layout.addLayout(self.length_lay)
		self.main_layout.addLayout(self.width_lay)
		self.main_layout.addLayout(self.height_lay)
		self.main_layout.addLayout(self.block_lay)
		self.main_layout.addLayout(self.gap_lay)
		self.main_layout.addLayout(self.street_lay)

		"""Stretch space between above Elements and below Elements"""
		self.main_layout.addStretch()

		"""Bottom Button Layout"""
		self.main_layout.addLayout(self.bottom_btn_lay)
		self.setLayout(self.main_layout)

	def create_connections(self):
		"""Connect our widgets signals to slots"""
		self.cancel_btn.clicked.connect(self.cancel)
		self.gen_btn.clicked.connect(self.gen)

	def _populate_scenefile_properties(self):
		"""Populates the SceneFile object's properties from the UI"""
		self.scene.length = self.length_spinbox.value()
		self.scene.width = self.width_spinbox.value()
		self.scene.max_height = self.height_spinbox.value()
		self.scene.block = self.block_spinbox.value()
		self.scene.gap = self.gap_spinbox.value()
		self.scene.street_width = self.street_spinbox.value()

	@QtCore.Slot()
	def cancel(self):
		"""Quits the dialog"""

		self.close()

	@QtCore.Slot()
	def gen(self):
		"""Activates the city generation script"""
		self._populate_scenefile_properties()
		print(self.scene.city_generator())
		self.scene.city_generator()

		"""Saves the scene into the scenes folder"""
		if self.save_btn.isChecked() == True:
			self.scene_save.increment_and_save()