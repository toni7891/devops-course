const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

function cpuStress() {
  let result = 0;
  for (let i = 0; i < 1e7; i++) result += Math.sqrt(i);
  return result;
}

function memoryStress() {
  const arrays = [];
  for (let i = 0; i < 50; i++) {
    arrays.push(new Array(1e6).fill(Math.random()));
  }
  return arrays.length;
}

app.get('/', (req, res) => res.send('Hello from ECR!\n'));

app.get('/cpu', (req, res) => {
  cpuStress();
  res.send('CPU stress done!\n');
});

app.get('/memory', (req, res) => {
  memoryStress();
  res.send('Memory stress done!\n');
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));