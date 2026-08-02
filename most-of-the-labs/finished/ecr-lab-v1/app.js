const express = require('express');

const app = express();
const PORT = process.env.PORT || 3000;

const jokes = [
  { id: 1, setup: "Why don't scientists trust atoms?", punchline: "Because they make up everything!" },
  { id: 2, setup: "Why did the scarecrow win an award?", punchline: "Because he was outstanding in his field!" },
  { id: 3, setup: "Why don't eggs tell jokes?", punchline: "They'd crack each other up!" },
  { id: 4, setup: "What do you call a fish without eyes?", punchline: "A fsh!" },
  { id: 5, setup: "Why can't you give Elsa a balloon?", punchline: "Because she'll let it go!" },
  { id: 6, setup: "What do you call cheese that isn't yours?", punchline: "Nacho cheese!" },
  { id: 7, setup: "Why did the math book look so sad?", punchline: "Because it had too many problems!" },
  { id: 8, setup: "What do you call a sleeping dinosaur?", punchline: "A dino-snore!" },
];

// GET hello
app.get('/', (req, res) => {
  res.json({ message: 'Hello from ECR container!' });
});

// GET all jokes
app.get('/jokes', (req, res) => {
  res.json(jokes);
});

// GET random joke
app.get('/jokes/random', (req, res) => {
  const joke = jokes[Math.floor(Math.random() * jokes.length)];
  res.json(joke);
});

// GET joke by id
app.get('/jokes/:id', (req, res) => {
  const joke = jokes.find(j => j.id === parseInt(req.params.id));
  if (!joke) return res.status(404).json({ error: 'Joke not found' });
  res.json(joke);
});

app.listen(PORT, () => {
  console.log(`Jokes API running on port ${PORT}`);
});
