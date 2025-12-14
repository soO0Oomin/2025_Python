import os

base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "phones.txt")

outfile = open(file_path, "w", encoding="utf-8")

outfile.write("홍길동3")
outfile.write("김철수2")
outfile.write("김영희3")

outfile.close()