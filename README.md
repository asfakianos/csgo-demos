# CSGO-Demos  

A '20 summer project using [Saul's NodeJS demo parser](https://github.com/saul/demofile) to take a CSGO `.dem` file and transform it into a feather dataframe for later use. Currently [js/app.js](js/app.js) accepts a `.dem` file and writes to a file that matches the name with a `.out` extension, enumerating all damage and kill events in post-warmup play. Then, [python/clean.py](python/clean.py) accepts a `.out` file and reads it to a `.feather` file, which uses the *pandas to_feather* method to transform the pseudo-csv file (`.out`) to the feather format.  

**Example:**  
![Example output](sample.png)

Blue spots represent locations where players died, and orange spots represent locations where players killed from.


## Work Log  
* **Jun 8** First prototype completed for graphing a match played on CSGO's Overpass map.  
  * Involves data flow from a NodeJS platform to generate a .out file that is faster to parse than the original .dem file, and a Python script to convert the .out file to a usable format (in this case, a pandas df -> feather format saved to file). A second Python script converts the feather file to a matplotlib plot. As of Jun 8, this process is only working on Overpass.  
* **Jun 14** Reformatted code into a single class file. The class expects a single `.out` file to be specified, and will generate a dataframe with an option for saving to a `.feather` format. See [csgodem.py](python/csgodem.py).