function greet(name) {
  if (!name) throw new Error("Name is required");
  return `Hello, ${name}!`;
}

module.exports = { greet };
