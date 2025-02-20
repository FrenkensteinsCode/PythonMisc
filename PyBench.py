from multiprocessing import Pool
import os
import time
from tqdm import tqdm

## CPU Benchmark
# Calculation to find prime numbers up to a certain limit
def sieve_segment(start, end):
    sieve = [True] * (end - start)
    for i in range(2, int(end ** 0.5) + 1):
        for j in range(max(i * i, (start + i - 1) // i * i), end, i):
            sieve[j - start] = False
    return [num for num, is_prime in enumerate(sieve, start) if is_prime and num > 1]

def find_primes(limit):
    num_processes = 12
    segment_size = (limit // num_processes) + 1
    segments = [(i * segment_size, min((i + 1) * segment_size, limit)) for i in range(num_processes)]

    with Pool(processes=num_processes) as pool:
        results = pool.starmap(sieve_segment, segments)

    primes = [prime for segment in results for prime in segment]
    return primes

# Generate list of primes in order to benchmark the CPU
def cpu_benchmark(limit: int):
    t0 = time.perf_counter()
    find_primes(limit)
    t1 = time.perf_counter()
    return t1 - t0

def exec_cpu_benchmark(limit: int, repeats: int, output_file: str):
    list_of_results = []
    with open(output_file, 'w') as f:
        for _ in tqdm(range(repeats), desc="Benchmarking"):
            result = cpu_benchmark(limit)
            list_of_results.append(result)
        avg = sum(list_of_results) / repeats

        f.write(f"*****CPU-BENCHMARK*****\n")
        f.write(f"Values per run: {list_of_results}\n")
        f.write(f"Averaged calculation time over {repeats} runs is: {avg:.4f}s\n")

        print(f"*****CPU-BENCHMARK*****")
        print(f"Averaged calculation time over {repeats} runs is: {avg:.4f}s")
        print(f"See {output_file} for details.")

## IO Benchmark
def write_benchmark(file_name, data_size):
    t0 = time.perf_counter()
    with open(file_name, 'w') as f:
        f.write('x' * data_size)
    t1 = time.perf_counter()
    return t1 - t0

def read_benchmark(file_name):
    t0 = time.perf_counter()
    with open(file_name, 'r') as f:
        f.read()
    t1 = time.perf_counter()
    return t1 - t0

def exec_io_benchmark(test_file: str, data_size: int, output_file: str):
    with open(output_file, 'a') as f:
        write_time = write_benchmark(test_file, data_size)
        read_time = read_benchmark(test_file)

        f.write(f"*****IO-BENCHMARK*****\n")
        f.write(f"Write: {write_time:.4f}s\n")
        f.write(f"Read: {read_time:.4f}s")

        print(f"*****IO-BENCHMARK*****")
        print(f"Write: {write_time:.4f}s")
        print(f"Read: {read_time:.4f}s")

        os.remove(test_file)

if __name__ == "__main__":
    limit = 10000000  # To which limit should we find prime numbers
    repeats = 100 # How many runs should we do
    data_size = 10**6  # 1 MB
    test_file = "benchmark.txt"
    out_file = "results.txt"

    exec_cpu_benchmark(limit, repeats, out_file)
    exec_io_benchmark(test_file, data_size, out_file)