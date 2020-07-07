#!/usr/local/bin/node
/**
 * Takes a demo file location as a command line argument and parses weapon damage and kills
 **/

const fs = require("fs");
const demofile = require("demofile");

let fname = process.argv[process.argv.length - 1];
let fout = fname.replace(".dem", ".out");

let killEventCount = 0;
let hurtEventCount = 0;

fs.writeFile(fout, `${fout}\n`, e => {
	if (e) throw e;
	console.log(`Created ${fout}`);
});
try {
	// Parses the demo file given as a command line argument
	fs.readFile(fname, (err, buffer) => {
	  const demoFile = new demofile.DemoFile();

	  // Log metadata on the match
	  demoFile.on("start", () => {
	  	fs.appendFile(fout, `${demoFile.header['mapName']}\n`, e=> {
	  		if (e) throw e;
	  	});
	  });

	  // Logging all instances of a player death
	  demoFile.gameEvents.on("player_death", e => {
	    if (!demoFile.gameRules.isWarmup) {
	      killEventCount += 1;
	      const target = demoFile.entities.getByUserId(e.userid);
	      const targetName = target ? target.name : "unnamed";
	      const targetPos = target ? `${x_to_res(target.position.x)},${y_to_res(target.position.y)}` : "NAN";

	      const attacker = demoFile.entities.getByUserId(e.attacker);
	      const attName = attacker ? attacker.name : "unnamed";
	      const attPos = attacker ? `${x_to_res(attacker.position.x)},${y_to_res(attacker.position.y)}` : "NAN";

	      const isHS = e.headshot ? " HS" : "";
	      const isWB = e.penetrated > 0 ? " WB" : "";

	      fs.appendFile(fout, `KILL/!${attName}/!${attPos}/!${e.weapon}${isHS}${isWB}/!${targetName}/!${targetPos}\n`, e => {
	      	if (e) throw e;
	      });
	      // console.log(`KILL/!${attName}/!${attPos}/!${e.weapon}${isHS}${isWB}/!${targetName}/!${targetPos}`);
	    }
	  });

	  // Logging all instances of a player taking damage in response to shooting
	  demoFile.gameEvents.on("player_hurt", e => {
	    if (!demoFile.gameRules.isWarmup) {
	      hurtEventCount += 1;

	      const target = demoFile.entities.getByUserId(e.userid);
	      const targetName = target ? target.name : "unnamed";
	      const targetPos = target ? `${x_to_res(target.position.x)},${y_to_res(target.position.y)}` : "NAN";

	      const attacker = demoFile.entities.getByUserId(e.attacker);
	      const attName = attacker ? attacker.name : "unnamed";
	      const attPos = attacker ? `${x_to_res(attacker.position.x)},${y_to_res(attacker.position.y)}` : "NAN";

	      fs.appendFile(fout, `DMG/!${attName}/!${attPos}/!${e.weapon}/!${targetName}/!${targetPos}/!${e.dmg_health}\n`, e => {
	      	if (e) throw e;
	      });
	      // console.log(`DMG/!${attName}/!${attPos}/!${e.weapon}/!${targetName}/!${targetPos}/!${e.dmg_health}`);
	    }
	  });

	  // Taking note of round end (and score) just for sanity purposes
	  demoFile.gameEvents.on("round_officially_ended", e => {
	    const teams = demoFile.teams;

	    const terrorists = teams[2];
	    const cts = teams[3];

	    console.log(`END: \tTerrorists: ${terrorists.clanName} score ${terrorists.score}\n\tCTs: ${cts.clanName} score ${cts.score}`);
	    fs.appendFile(fout, `/!ROUND/!\n`, e=> {
	    	if (e) throw e;
	    }); // end of round
	  });

	  demoFile.parse(buffer);
	});
} catch (e) {
	console.log("Encountered an error when trying to open the specified demo file.");
	console.error(e);
}

// WIP - Ideally these should normalize the coordinates from the demo to fit a map, but this'll likely be moved to Python once I figure out the mapping
// UPDATE: These dimensions are perfect for de_mirage, currently working on scaling for other maps
function x_to_res(xinput) {
  const startX = -3217;
  const endX = 1912;
  // Adjust to fit size of image resolution
  const resX = 100;

  let sizeX = endX-startX;

  if (startX < 0)
    xinput +=  (startX * -1.0);
  else
    xinput += startX;

  xoutput = (xinput / Math.abs(sizeX)) * resX;
  return (xoutput).toFixed(3);
}

function y_to_res(yinput) {
  const startY = -3401;
  const endY = 1682;
  // Adjust to fit size of image
  const resY = 100;

  let sizeY = endY-startY;

  if (startY < 0)
    yinput += (startY * -1.0);
  else
    yinput += startY;

  youtput = (yinput / Math.abs(sizeY)) * resY;
  return (youtput).toFixed(3);
}
