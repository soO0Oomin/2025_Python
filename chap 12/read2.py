import os

base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "phones.txt")

infile = open(file_path, "r", encoding="utf-8")
for line in infile:
    line = line.rstrip()
    print(line)

infile.close()