'use strict';

const { add, multiply } = require('../src/utils/math');

describe('add()', () => {
  it('sums two positive numbers', () => expect(add(2, 3)).toBe(5));
  it('handles negative numbers', () => expect(add(-1, 1)).toBe(0));
  it('throws on non-numbers', () => expect(() => add('a', 1)).toThrow(TypeError));
});

describe('multiply()', () => {
  it('multiplies two numbers', () => expect(multiply(3, 4)).toBe(12));
  it('returns 0 when either operand is 0', () => expect(multiply(5, 0)).toBe(0));
  it('throws on non-numbers', () => expect(() => multiply(null, 2)).toThrow(TypeError));
});
