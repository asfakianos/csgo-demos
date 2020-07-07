#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
# ^ Update for your own usage. This is my own path for testing purposes

import sys
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker
import re

DELIM="/!"
HEADER=["EVENTTYPE", "ATTNAME", "ATTPOS", "HOW", "TARNAME", "TARPOS", "DMG"]
# A lot of these are stretched, and it'd make more sense to normalize the images (common center) and modify app.js, but whatever
MAP_EXTENT={
	"de_dust2":[15,103,33,133],
	"de_overpass":[-30,70,0,100], 
	"de_mirage":[0,100,0,100],
	"de_train":[10,110,16.5,116.5],
	"de_nuke":[9,124,-14,116],
	"de_vertigo":[-30,70,0,100], #TODO
	"de_cache":[-30,70,0,100], #TODO
	"de_inferno":[21,121,43,143]
}

def clean(fname, save=False):
	"""If save is set to True, the data will be saved in the .feather format and returned. If save is set to False, the data will only be returned"""
	try:
		# Need to specify engine as python due to our delimiter being > 1 (so the c engine won't work...)
		fout = pd.read_csv(fname, delimiter=DELIM, skiprows=2, engine='python',
						   header=None,
						   names=HEADER
						   )
		fout = fout[fout.ATTPOS != ("NAN" or "ATTPOS")] # Removing 'empty' rows
		fout = fout.reset_index() # Reset index to fix index of removed rows

		# Save the data with to_feather
		if save:
			outName = fname.split(".")[0] + ".feather"
			print(outName)
			fout.to_feather(outName)

			print("\tSaved file to " + outName + " in feather format!") # Debug

		return fout

	except:
		print(f"ran into an I/O issue with given file: {fname}")


class CSGODem:

	# Loading the data into a pandas dataframe to enable use otherwise
	def __init__(self, outfile, save=False):
		"""Accepts an outfile (.out) and extracts meta data before parsing the data and creating a dataframe.
		If this is ever modified to be something more than just hltv parsing, this sort of assumption for team names, map will need to be changed. """

		self.save = save

		# Extracting metadata from the first line of the file
		with open(outfile, 'r') as file:
			self.fname = file.readline()[:-5]
			self.map_name = file.readline().strip() # app.js sets the 2nd line to CSGO's name for the map

		# Leave saving up to the user's input.
		self.data = clean(outfile, save=self.save)

	def entries(self):
		try:
			data = self.data



	def graph(self):
		try:
			data = self.data
			# data.header = HEADER
			attpos = data.ATTPOS.str.split(",",expand=True)
			tarpos = data.TARPOS.str.split(",",expand=True)

			# Convert to numpy array for plotting
			# Since names don't matter (right now), just use coord pairs
			attx = attpos[0].astype(float).to_numpy()
			atty = attpos[1].astype(float).to_numpy()

			tarx = tarpos[0].astype(float).to_numpy()
			tary = tarpos[1].astype(float).to_numpy()

			img = plt.imread(f"../maps/{self.map_name}.png")

			fig,ax = plt.subplots()

			current_map_extent = MAP_EXTENT[self.map_name]
			# scaled_extent = [i * SCALE for i in current_map_extent]

			plt.xlim(current_map_extent[0], current_map_extent[1])
			plt.ylim(current_map_extent[2], current_map_extent[3])

			ax.imshow(img, extent=current_map_extent)

			ax.scatter(attx, atty, color='orange', alpha=0.1)
			ax.scatter(tarx, tary, color='blue', alpha=0.1)

			# Enable no ticks:
			ax.get_xaxis().set_major_locator(ticker.NullLocator())
			ax.get_yaxis().set_major_locator(ticker.NullLocator())

			# If save, save an image of the plot
			if self.save:
				plt.savefig(f"{self.fname}.png", bbox_inches="tight", dpi=400)

			plt.show()

		except:
			print("The object was not initialized correctly. Data might be missing post-init")


	def __str__(self):
		return f"{self.map_name} from {self.fname}"


def main(fname):
	dem = CSGODem(fname, save=True)
	print("Loaded " + str(dem))
	dem.graph()

if __name__ == '__main__':
	"""Expects stdin args in the format of ./csgodem.py <FILENAME>."""
	main(sys.argv[1])
