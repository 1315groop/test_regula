Solution Description

This solution implements a system to generate unique file paths, store them in a PostgreSQL database, and track their processing status using a Bloom filter. PostgreSQL's native Bloom filter extension is utilized to efficiently check file presence while minimizing memory usage and false positives. The script performs the following operations:

Generates N unique file paths.

Inserts file paths into a PostgreSQL database.

Uses a Bloom filter index to optimize search queries.

Marks files as processed and checks their status.

Measures the execution time of path generation and lookup operations.

Calculates memory usage for filenames and the Bloom filter.

Launch Instructions

run containers from docker-compose

Run the script:

python main.py

Measurement Results for the Selected N

For N = 100, the following performance metrics were recorded:

Path generation time: 0.008241 seconds

Check time (added): 0.007642 seconds

Check time (not added): 0.007649 seconds

Memory occupied by file names: 29600 bytes

Memory used by Bloom filter: 24 kB

Justification of the Selected Bloom Filter Parameters

for length: 
Larger sizes reduce false positives but use more memory

Rule of thumb: Start with length = 10 × number of distinct values so 1000 in our case

for col1:
More bits per column reduces false positives

For text columns like filenames: 4-5 bits often works well