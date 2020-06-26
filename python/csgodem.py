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

def clean(fname, save=False):
	"""If save is set to True, the data will be saved in the .feather format and returned. If save is set to False, the data will only be returned"""
	try:
		# Need to specify engine as python due to our delimiter being > 1 (so the c engine won't work...)
		fout = pd.read_csv(fname, delimiter=DELIM, skiprows=1, engine='python',
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

		self.team1 = ""
		self.team2 = ""
		# Extracting metadata from the first line of the file
		with open(outfile, 'r') as file:
			try:
				line1 = file.readline()
				# Grab the team names and map name from the first line of the .out file provided.
				team_split = re.split(r"\-vs\-", re.split(r"/", line1)[2]) # Initial splits create a single team name @0 and a combination of teamname and mapname.out @1
				# Replacing all non-alphanum chars with spaces in the first team name
				self.team1 = re.sub(r"[^\w]+", " ", team_split[0])
				# Something similar for the second team name and map
				team_split = re.split(r"[^\w]+", re.split(r".out", team_split[1])[0])
				self.map_name = team_split[-1] # The map names are always one word and should always show up at the end of the string in these cases.
				self.team2 = " ".join(team_split[:-1]) # Team names should occupy all other locations
			except:
				print("first line wasn't formatted as expected. Using the filename as the only metadata")
				self.map_name = outfile

		# Leave saving up to the user's input.
		self.data = clean(outfile, save=save)

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

			plt.xlim(-30,70)
			plt.ylim(0,100)

			ax.imshow(img, extent=[-30,70,0,100])

			ax.scatter(attx, atty, color='orange', alpha=0.1)
			ax.scatter(tarx, tary, color='blue', alpha=0.1)

			# Enable no ticks:
			ax.get_xaxis().set_major_locator(ticker.NullLocator())
			ax.get_yaxis().set_major_locator(ticker.NullLocator())

			plt.show()
		except:
			return "The object was not initialized correctly. Data might be missing post-init"


	def __str__(self):
		try:
			return f"{self.team1} vs {self.team2} on {self.map_name}."
		except:
			return "Team names and/or map not properly initialized."


def main(fname):
	dem = CSGODem(fname)
	print("Loaded " + dem)
	dem.graph()

if __name__ == '__main__':
	"""Expects stdin args in the format of ./csgodem.py <FILENAME>."""
	main(sys.argv[1])
