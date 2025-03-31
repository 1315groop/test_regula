import sys
import time

import psycopg2
from typing import List

from test_regula.utils import generate_unique_filenames

DB_CONFIG = {
    "dbname": "mydatabase",
    "user": "user",
    "password": "password",
    "host": "postgres_db",
    "port": "5432"
}


def create_table():
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE EXTENSION IF NOT EXISTS bloom;
                CREATE TABLE IF NOT EXISTS files (
                    id SERIAL PRIMARY KEY,
                    filename TEXT UNIQUE NOT NULL,
                    processed BOOLEAN DEFAULT FALSE
                );
                CREATE INDEX IF NOT EXISTS files_bloom_idx ON files USING bloom (filename) WITH (length=1000, col1=4);
            """)
            conn.commit()


def insert_filenames(filenames: List[str]):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            for filename in filenames:
                cur.execute("""
                    INSERT INTO files (filename) VALUES (%s)
                    ON CONFLICT (filename) DO NOTHING
                """, (filename,))
            conn.commit()


def mark_as_processed(filename: str):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE files SET processed = TRUE WHERE filename = %s
            """, (filename,))
            conn.commit()


def is_processed(filename: str) -> bool:
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT processed FROM files WHERE filename = %s
            """, (filename,))
            result = cur.fetchone()
            return result[0] if result else False

def get_bloom_filter_size():
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT pg_size_pretty(pg_relation_size('files_bloom_idx'));")
            return cur.fetchone()[0]

def main():
    create_table()

    start_time = time.time()
    filenames = generate_unique_filenames(100)
    path_gen_time = time.time() - start_time

    insert_filenames(filenames)

    # Simulating file processing
    for filename in filenames[:50]:  # Mark first 50 as processed
        mark_as_processed(filename)

    # Measuring check time
    test_filename = filenames[0]
    start_time = time.time()
    _ = is_processed(test_filename)
    check_time_added = time.time() - start_time

    start_time = time.time()
    _ = is_processed("non_existent_file")
    check_time_not_added = time.time() - start_time

    # Memory calculations
    filenames_memory = sum(sys.getsizeof(f) for f in filenames)
    bloom_filter_size = get_bloom_filter_size()

    # Output results
    print(f"Path generation time: {path_gen_time:.6f} seconds")
    print(f"Check time (added): {check_time_added:.6f} seconds")
    print(f"Check time (not added): {check_time_not_added:.6f} seconds")
    print(f"Memory occupied by file names: {filenames_memory} bytes")
    print(f"Memory used by Bloom filter: {bloom_filter_size}")

    # Check file statuses
    for filename in filenames:
        print(f"{filename} - {'Processed' if is_processed(filename) else 'Not Processed'}")


if __name__ == "__main__":
    main()

