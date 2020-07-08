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
	  demoFile.gameEvents.on("weapon_fire", e => {
	  	const shooter = demoFile.entities.getByUserId(e.userid);
	  	console.log(`${shooter.name} fired`);
	  });

	  // Logging all instances of a player taking damage in response to shooting
	  demoFile.gameEvents.on("player_hurt", e => {
	  	const target = demoFile.entities.getByUserId(e.userid);
	  	const shooter = demoFile.entities.getByUserId(e.attacker);
	  	console.log(`${target.name} was hit by ${shooter.name} for ${e.dmg_health} with ${e.weapon} in the ${e.hitgroup}`);
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

