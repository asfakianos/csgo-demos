#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
# ^ Update for your own usage. This is my own path for testing purposes

import sys
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker

# Modified header as we are splitting the df to x,y rather than just POS
HEADER=["EVENTTYPE", "ATTNAME", "ATTPOS", "HOW", "TARNAME", "TARPOS", "DMG"]

def graph(fname):
	# Initializing dataset from given datafile
	data = pd.read_feather(fname)
	# data.header = HEADER
	attpos = data.ATTPOS.str.split(",",expand=True)
	tarpos = data.TARPOS.str.split(",",expand=True)

	# Convert to numpy array for plotting
	# Since names don't matter (right now), just use coord pairs
	attx = attpos[0].astype(float).to_numpy()
	atty = attpos[1].astype(float).to_numpy()

	# for x,y in zip(attx,atty):
	# 	print(x,y)

	tarx = tarpos[0].astype(float).to_numpy()
	tary = tarpos[1].astype(float).to_numpy()

	# for tup in defpos:
	# 	print(tup)


	img = plt.imread("../maps/overpass.png")

	fig,ax = plt.subplots()

	plt.xlim(-30,70)
	plt.ylim(0,100)

	ax.imshow(img, extent=[-30,70,0,100])

	ax.scatter(attx, atty, color='orange', alpha=0.1)
	ax.scatter(tarx, tary, color='blue', alpha=0.1)

	# Enable 12 major tick marks (12 ticks results in a 0 tick, 100 tick + 10 ticks in between)
	# ax.get_xaxis().set_major_locator(ticker.LinearLocator(12))
	# ax.get_yaxis().set_major_locator(ticker.LinearLocator(12))
	# Enable no ticks:
	ax.get_xaxis().set_major_locator(ticker.NullLocator())
	ax.get_yaxis().set_major_locator(ticker.NullLocator())

	plt.show()

if __name__ == '__main__':
	graph(sys.argv[1])
