/**
 * Takes a demo file location as a command line argument and parses weapon damage and kills
 **/

const fs = require("fs");
const demofile = require("demofile");

fname = process.argv[process.argv.length - 1];

let killEventCount = 0;
let hurtEventCount = 0;

// Parses the demo file given as a command line argument
fs.readFile(fname, (err, buffer) => {
  const demoFile = new demofile.DemoFile();

  // Logging all instances of a player death
  demoFile.gameEvents.on("player_death", e => {
    if (!demoFile.gameRules.isWarmup) {
      killEventCount += 1;
      const target = demoFile.entities.getByUserId(e.userid);
      const targetName = target ? target.name : "unnamed";
      const targetPos = target ? `(${x_to_res(target.position.x)},${y_to_res(target.position.y)})` : "()";

      const attacker = demoFile.entities.getByUserId(e.attacker);
      const attName = attacker ? attacker.name : "unnamed";
      const attPos = attacker ? `(${x_to_res(attacker.position.x)},${y_to_res(attacker.position.y)})` : "()";

      const isHS = e.headshot ? " HS" : "";
      const isWB = e.penetrated > 0 ? " WB" : "";

      console.log(`KILL/!${attName}/!${attPos}/!${e.weapon}${isHS}${isWB}/!${targetName}/!${targetPos}`);
    }
  });

  // Logging all instances of a player taking damage in response to shooting
  demoFile.gameEvents.on("player_hurt", e => {
    if (!demoFile.gameRules.isWarmup) {
      hurtEventCount += 1;

      const target = demoFile.entities.getByUserId(e.userid);
      const targetName = target ? target.name : "unnamed";
      const targetPos = target ? `(${x_to_res(target.position.x)},${y_to_res(target.position.y)})` : "()";

      const attacker = demoFile.entities.getByUserId(e.attacker);
      const attName = attacker ? attacker.name : "unnamed";
      const attPos = attacker ? `(${x_to_res(attacker.position.x)},${y_to_res(attacker.position.y)})` : "()";

      console.log(`DMG/!${attName}/!${attPos}/!${e.weapon}/!${targetName}/!${targetPos}/!${e.dmg_health}`);
    }
  });

  // Taking note of round end (and score) just for sanity purposes
  demoFile.gameEvents.on("round_officially_ended", e => {
    const teams = demoFile.teams;

    const terrorists = teams[2];
    const cts = teams[3];

    console.log(
      "END: \tTerrorists: %s score %d\n\tCTs: %s score %d",
      terrorists.clanName,
      terrorists.score,
      cts.clanName,
      cts.score
    );
    console.log(`\nkills: ${killEventCount}\nHurt: ${hurtEventCount}`);
  });

  demoFile.parse(buffer);
});

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
