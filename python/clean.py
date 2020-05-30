#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
# ^ Update for your own usage. This is my own path for testing purposes

import sys
import os
import numpy as np
import pandas as pd

DELIM="/!"

def main(fname):
	try:
		# Need to specify engine as python due to our delimiter being > 1 (so the c engine won't work...)
		fout = pd.read_csv(fname, delimiter=DELIM, skiprows=1, engine='python', 
						   header=None, 
						   names=["EVENTTYPE", "ATTNAME", "ATTPOS", "HOW", "TARNAME", "TARPOS", "DMG"]
						   )
		print("\tSuccesfully read csv!") # Debug
		print(fout) # Debug
		outName = fname.split(".")[0] + ".feather"
		fout.to_feather(outName)
		print("\tSaved file to " + outName + " in feather format!") # Debug
	except:
		print(f"ran into an I/O issue with given file: {fname}")


if __name__ == '__main__':
	main(sys.argv[1])
