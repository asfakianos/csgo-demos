#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
# ^ Update for your own usage. This is my own path for testing purposes

import sys
import os
import numpy as np
import pandas as pd

DELIM="/!"
HEADER=["EVENTTYPE", "ATTNAME", "ATTPOS", "HOW", "TARNAME", "TARPOS", "DMG"]

def save(fname):
	try:
		# Need to specify engine as python due to our delimiter being > 1 (so the c engine won't work...)
		fout = pd.read_csv(fname, delimiter=DELIM, skiprows=1, engine='python', 
						   header=None, 
						   names=HEADER
						   )
		fout = fout[fout.ATTPOS != ("NAN" or "ATTPOS")] # Removing 'empty' rows
		fout = fout.reset_index() # Reset index to fix index of removed rows

		##
		# DEBUG
		##
		print("\tSuccesfully read csv!") 
		# pd.set_option('display.max_rows', None)
		print(fout) 

		outName = fname.split(".")[0] + ".feather"
		print(outName)
		fout.to_feather(outName)

		print("\tSaved file to " + outName + " in feather format!") # Debug
	except:
		print(f"ran into an I/O issue with given file: {fname}")


if __name__ == '__main__':
	save(sys.argv[1])
