const { greet } = require('../src/greet');

test('greets by name', () => {
  expect(greet('World')).toBe('Hello, World!');
});

test('throws when name is empty', () => {
  expect(() => greet('')).toThrow('Name is required');
});
