const express = require('express');
const app = express();
const PORT = 3000;

const movies = [
  { title: 'The Shawshank Redemption', genre: 'Drama', year: 1994, rating: 9.3 },
  { title: 'The Godfather', genre: 'Crime', year: 1972, rating: 9.2 },
  { title: 'The Dark Knight', genre: 'Action', year: 2008, rating: 9.0 },
  { title: 'Pulp Fiction', genre: 'Crime', year: 1994, rating: 8.9 },
  { title: 'Forrest Gump', genre: 'Drama', year: 1994, rating: 8.8 },
  { title: 'Inception', genre: 'Sci-Fi', year: 2010, rating: 8.8 },
  { title: 'The Matrix', genre: 'Sci-Fi', year: 1999, rating: 8.7 },
  { title: 'Interstellar', genre: 'Sci-Fi', year: 2014, rating: 8.6 },
  { title: 'Goodfellas', genre: 'Crime', year: 1990, rating: 8.7 },
  { title: 'Fight Club', genre: 'Drama', year: 1999, rating: 8.8 },
  { title: 'The Silence of the Lambs', genre: 'Thriller', year: 1991, rating: 8.6 },
  { title: 'Schindler\'s List', genre: 'Drama', year: 1993, rating: 9.0 },
  { title: 'The Lord of the Rings: The Return of the King', genre: 'Fantasy', year: 2003, rating: 9.0 },
  { title: 'Parasite', genre: 'Thriller', year: 2019, rating: 8.5 },
  { title: 'Oppenheimer', genre: 'Drama', year: 2023, rating: 8.9 },
];

app.get('/', (req, res) => {
  const movie = movies[Math.floor(Math.random() * movies.length)];
  res.json({
    version: 'v3',
    message: 'Here is your movie recommendation!',
    recommendation: movie,
  });
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok', version: 'v2' });
});

app.listen(PORT, () => {
  console.log(`Movie Recommendation API v2 running on port ${PORT}`);
});
