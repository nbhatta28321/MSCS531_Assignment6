import threading
import time
import os

# Define configurations for the latency design space exploration.
# Each tuple represents (opLat, issueLat) where the sum must be 7.
latency_configurations = [
    (1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)
]

# Simulation parameters
n = 1000000  # Size of the vector for the daxpy operation
a = 2.0  # Scalar multiplier
num_threads_list = [2, 4, 8]  # Number of threads to test

# Multi-threaded daxpy kernel function
def daxpy_thread(x, y, start, end, opLat, issueLat):
    for i in range(start, end):
        y[i] = a * x[i] + y[i]
        # Simulate operation and issue latency
        time.sleep(opLat * 0.0001)  # Simulated operation latency
        time.sleep(issueLat * 0.0001)  # Simulated issue latency

# Run the daxpy kernel with different configurations and thread counts
def run_simulation(opLat, issueLat, num_threads):
    # Initialize input vectors
    x = [i * 0.5 for i in range(n)]
    y = [i * 0.3 for i in range(n)]

    # Divide workload among threads
    step = n // num_threads
    threads = []
    
    # Start timing
    start_time = time.time()
    
    # Create and start threads
    for i in range(num_threads):
        start_index = i * step
        end_index = n if i == num_threads - 1 else (i + 1) * step
        thread = threading.Thread(target=daxpy_thread, args=(x, y, start_index, end_index, opLat, issueLat))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # End timing
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"Configuration (opLat={opLat}, issueLat={issueLat}), Threads={num_threads}")
    print(f"  Total Execution Time: {total_time:.2f} seconds\n")

# Run simulations for each configuration and thread count
for opLat, issueLat in latency_configurations:
    for num_threads in num_threads_list:
        run_simulation(opLat, issueLat, num_threads)

print("All simulations complete.")
