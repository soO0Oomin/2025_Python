import os

base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "proverbs.txt")

infile = open(file_path)

outfile = open("output.txt","w")

i=1

for line in infile:
    outfile.write(str(i) + ":" + line)

    i=i+1

infile.close()
outfile.close()