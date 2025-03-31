import random
import string
import math
import hashlib
import time
import sys

from test_regula.utils import generate_unique_filenames, generate_filename


class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.byte_array = bytearray((size + 7) // 8)

    def add(self, strin):
        for seed in range(self.hash_count):
            hash_val = self._hash(strin, seed) % self.size
            byte_index = hash_val // 8
            bit_index = hash_val % 8
            self.byte_array[byte_index] |= (1 << bit_index)

    def contains(self, strin):
        for seed in range(self.hash_count):
            hash_val = self._hash(strin, seed) % self.size
            byte_index = hash_val // 8
            bit_index = hash_val % 8
            if not (self.byte_array[byte_index] & (1 << bit_index)):
                return False
        return True

    def _hash(self, strin, seed):
        h = hashlib.sha256()
        h.update((str(seed) + strin).encode('utf-8'))
        return int(h.hexdigest(), 16)

    @classmethod
    def optimal_filter(cls, items_count, fp_prob):
        size = - (items_count * math.log(fp_prob)) / (math.log(2) ** 2)
        size = int(size)
        hash_count = (size / items_count) * math.log(2)
        hash_count = int(hash_count)
        return cls(size, hash_count)

    def memory_usage(self):
        """Returns memory used by Bloom filter in bytes"""
        return sys.getsizeof(self.byte_array)


def measure_performance(N):
    print(f"\nPerformance metrics for N = {N}")
    print("=" * 50)

    # 1. Measure filename generation time
    start_time = time.time()
    filenames = generate_unique_filenames(N)
    gen_time = time.time() - start_time
    print(f"Filename generation time: {gen_time:.4f} seconds")

    # 2. Measure memory usage of filenames
    filenames_memory = sum(sys.getsizeof(name) for name in filenames)
    print(f"Memory used by filenames: {filenames_memory / 1024:.2f} KB")

    # 3. Create Bloom filter and measure memory
    bloom = BloomFilter.optimal_filter(N, 0.01)
    print(f"Bloom filter memory usage: {bloom.memory_usage() / 1024:.2f} KB")

    # 4. Measure time to add all filenames
    start_time = time.time()
    for name in filenames:
        bloom.add(name)
    add_time = time.time() - start_time
    print(f"Time to add all filenames: {add_time:.4f} seconds")

    # 5. Measure time to check existing filenames
    start_time = time.time()
    for name in filenames[:1000]:  # Check first 1000 for speed
        bloom.contains(name)
    exist_check_time = (time.time() - start_time) / 1000
    print(f"Time per check (existing): {exist_check_time:.6f} seconds")

    # 6. Measure time to check non-existing filenames
    start_time = time.time()
    for _ in range(1000):
        random_name = generate_filename()
        bloom.contains(random_name)
    non_exist_check_time = (time.time() - start_time) / 1000
    print(f"Time per check (non-existing): {non_exist_check_time:.6f} seconds")

    # 7. Calculate false positive rate
    false_positives = 0
    tests = 10000
    for _ in range(tests):
        random_name = generate_filename()
        if random_name not in filenames and bloom.contains(random_name):
            false_positives += 1
    fp_rate = false_positives / tests
    print(f"Actual false positive rate: {fp_rate:.4%}")


if __name__ == "__main__":
    # Test with different N values
    for N in [1000, 10000, 100000]:
        measure_performance(N)
        print("\n")