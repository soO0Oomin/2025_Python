import os

base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "proverbs.txt")

with open(file_path, "r") as file:
    for line in file:
        print(line.strip())