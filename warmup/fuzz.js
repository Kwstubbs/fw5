const { spawnSync } = require("node:child_process");
const { randomInt } = require("node:crypto");

let alphabet = "=";

for (let i = 0; i < 10000; i++) {
  alphabet += String.fromCharCode(i);
}

const failures = [];

const randStr = () =>
  Array.from(
    { length: randomInt(1, 100) },
    () => alphabet[randomInt(alphabet.length)],
  ).join("");

for (let i = 1; i <= 1000; i++) {
  const input = randStr() + '=' + randStr();
  const result = spawnSync("python3.11", ["./target.py"], {
    input,
    encoding: "utf8",
  });

  if (result.status) {
    console.log(`Crashed for ${JSON.stringify(input)}`);
  }
}

if (!failures.length) {
  console.log("No crashes!");
}
