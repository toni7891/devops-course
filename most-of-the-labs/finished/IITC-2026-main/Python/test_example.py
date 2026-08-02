# =============================================================================
# TESTING EXERCISE — Fix the Broken Tests!
# =============================================================================
#
# GOAL: Fix the broken tests below so they all pass.
#
# HOW TO RUN:
#   cd /Users/rwnhdd/PycharmProjects/IITC-2026/Python
#   pytest test_example.py -v
#
# RULES:
#   1. Tests are functions starting with "test_"
#   2. Use assert to check if something is True
#   3. Fix the assert statements so they match what the function returns


# =============================================================================
# FUNCTIONS (these work correctly, don't change them)
# =============================================================================

def add(a, b):
    """Adds two numbers together."""
    return a + b


def subtract(a, b):
    """Subtracts b from a."""
    return a - b


def multiply(a, b):
    """Multiplies two numbers."""
    return a * b


# =============================================================================
# BROKEN TESTS — Fix These!
# =============================================================================

def test_add():
    """
    This test is BROKEN. Fix the assert so it passes.
    Hint: add(2, 3) returns 5, not 6.
    """
    result = add(2, 3)
    assert result == 6  # FIXME: Change 6 to the correct answer


def test_subtract():
    """
    This test is BROKEN. Fix the assert so it passes.
    Hint: subtract(5, 3) returns 2, not 8.
    """
    result = subtract(5, 3)
    assert result == 8  # FIXME: Change 8 to the correct answer


def test_multiply():
    """
    This test is BROKEN. Fix the assert so it passes.
    Hint: multiply(4, 5) returns 20.
    """
    result = multiply(4, 5)
    assert result == 25  # FIXME: Change 25 to the correct answer


# =============================================================================
# YOUR TURN — Add a New Test!
# =============================================================================
#
# TODO: Add test_divide() that tests a divide(a, b) function.
#
# Step 1: Create the divide function above (return a / b)
# Step 2: Write test_divide() below with an assert
# Step 3: Run pytest test_example.py -v to see it pass
#
# Example:
#   def divide(a, b):
#       return a / b
#
#   def test_divide():
#       result = divide(10, 2)
#       assert result == 5