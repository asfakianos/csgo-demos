# CSGO-Demos  

A '20 summer project using [Saul's NodeJS demo parser](https://github.com/saul/demofile) to take a CSGO `.dem` file and transform it into a feather dataframe for later use. Currently [js/app.js](js/app.js) accepts a `.dem` file and writes to a file that matches the name with a `.out` extension, enumerating all damage and kill events in post-warmup play. Then, [python/clean.py](python/clean.py) accepts a `.out` file and reads it to a `.feather` file, which uses the *pandas* `to_feather` method to transform the pseudo-csv file (`.out`) to the feather format.  

**Example:**  
![Example output](sample.png)

Blue spots represent locations where players died, and orange spots represent locations where players killed from.


## Work Log  
* **Jun 8** First prototype completed for graphing a match played on CSGO's Overpass map.  
  * Involves data flow from a NodeJS platform to generate a .out file that is faster to parse than the original .dem file, and a Python script to convert the .out file to a usable format (in this case, a pandas df -> feather format saved to file). A second Python script converts the feather file to a matplotlib plot. As of Jun 8, this process is only working on Overpass.  
* **Jun 14** Reformatted code into a single class file. The class expects a single `.out` file to be specified, and will generate a dataframe with an option for saving to a `.feather` format. See [csgodem.py](python/csgodem.py).  
  * The class now parses the team names and map name from a properly generated `.out` file.  
* **Jun 26** Edited how metadata was generated (now in [app.js](js/app.js)) and added (readded?) the maps folder, now using CSGO's naming conventions (de_\*)  
  * When creating [app.js](app.js), I found code from a different demo-based app that normalized locations in a demo to a given scale. In this case, I'm trying to normalize to a 100x100 scale (which is very easy to change later on). It seems, however, that the normalization fits perfectly for *de_mirage* and isn't meant for other maps. I'm going to stretch the extents to fit, which will hopefully allow me to develop a scale for later usage.  
