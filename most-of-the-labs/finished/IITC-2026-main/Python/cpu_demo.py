"""
Multiprocessing demo: Good for CPU-bound tasks (calculations)
Run: python3 cpu_demo.py
"""
import multiprocessing
import time
import os

def calculate(n):
    """CPU-intensive calculation"""
    result = 0
    for i in range(n):
        result += i ** 2
    print(f"  Process {os.getpid()} completed calculation")
    return result

numbers = [5_000_000, 5_000_000, 5_000_000, 5_000_000]

# IMPORTANT: On macOS/Windows, multiprocessing code MUST be inside
# if __name__ == "__main__": block or it will hang/loop infinitely!
if __name__ == "__main__":
    print(f"CPU cores available: {multiprocessing.cpu_count()}")
    print()

    # Sequential version
    print("=== Sequential (1 process, 1 after another) ===")
    start = time.time()
    for n in numbers:
        calculate(n)
    seq_time = time.time() - start
    print(f"Total time: {seq_time:.1f}s\n")

    # Multiprocessing version
    print(f"=== Multiprocessing ({len(numbers)} workers) ===")
    print("  All 4 calculations run in parallel on different CPU cores!")
    start = time.time()
    with multiprocessing.Pool(4) as pool:
        pool.map(calculate, numbers)
    mp_time = time.time() - start
    print(f"Total time: {mp_time:.1f}s\n")

    # Summary
    speedup = seq_time / mp_time
    print(f"Speedup: {speedup:.1f}x faster with multiprocessing!")
    print("\nWhy? Python's GIL limits threads to 1 CPU core.")
    print("Multiprocessing creates separate processes, each with its own GIL.")
    print("This bypasses the GIL and uses all CPU cores!")

# =============================================================================
# CHALLENGE: Modify This Script
# =============================================================================
#
# CHALLENGE 1: Change the number of workers
#   Try changing Pool(4) to Pool(2) or Pool(8)
#   Watch how the time changes
#   Note: More workers than CPU cores doesn't help much
#
# CHALLENGE 2: Make the calculation heavier
#   Change 5_000_000 to 10_000_000
#   See both sequential and multiprocessing take longer
#   But multiprocessing is still ~4x faster
#
# CHALLENGE 3: Try with threading instead
#   Replace multiprocessing.Pool with:
#       from concurrent.futures import ThreadPoolExecutor
#       with ThreadPoolExecutor(4) as executor:
#           executor.map(calculate, numbers)
#   Watch how it's SLOWER than multiprocessing (GIL!)
#
# CHALLENGE 4: Use all CPU cores
#   Change Pool(4) to Pool(multiprocessing.cpu_count())
#   This uses all available cores automatically
