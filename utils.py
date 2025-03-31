import random
import string
from typing import List, Set


def generate_filename(length: int = 255) -> str:
    characters: str = string.ascii_letters + string.digits + '_-'
    return ''.join(random.choice(characters) for _ in range(length))


def generate_unique_filenames(n: int) -> List[str]:
    filenames: Set[str] = set()
    while len(filenames) < n:
        filename: str = generate_filename()
        filenames.add(filename)
    return list(filenames)


# if __name__ == "__main__":
#     N: int = 10
#     unique_filenames: List[str] = generate_unique_filenames(N)
#
#     for i, name in enumerate(unique_filenames[:5], 1):
#         print(f"Filename {i}: {name[:20]}... (length: {len(name)})")
