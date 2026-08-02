locals {
  # Math operators: *, /, +, -, %, -number
  math = 2 * 2

  # Equality operators: ==, !=
  equality = 2 != 2

  # Comparison operators: <, <=, >, >=
  comparison = 2 < 1

  # Logical operators: !, ||, &&
  logical = true || false
}

output "operators" {
  value = {
    math       = local.math
    equality   = local.equality
    comparison = local.comparison
    logical    = local.logical
  }
}