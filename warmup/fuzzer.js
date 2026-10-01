const { spawnSync } = require('child_process')
const { randomBytes, randomInt } = require('crypto')
const { writeFileSync } = require('fs')

const alphabet = Buffer.from('abc=123 \n')

for (let i = 0; i < 1000; i++) {
  const input = randomBytes(randomInt(1, 21)).map((b) => alphabet[b % alphabet.length])
  const { stderr } = spawnSync('python3.11', ['target.py'], { input })

  if (stderr.includes('ValueError')) {
    console.log('crash found', { i, input: input.toString() })
    console.log(stderr.toString())
    writeFileSync('crash.bin', input)
    process.exit(0)
  }
}

process.exit(1)