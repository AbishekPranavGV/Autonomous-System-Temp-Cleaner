
    const fs = require('fs');
    const vm = require('vm');
    const code = fs.readFileSync('scratch/test_block_1.js', 'utf-8');
    try {
      new vm.Script(code);
      console.log('Script block 1: SYNTAX VALID');
    } catch (e) {
      console.error('Script block 1 SYNTAX ERROR:', e.message);
      process.exit(1);
    }
    