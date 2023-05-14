from itertools import islice
import sys
from pprint import pprint as pp

def formatLine(line):
    return line.replace("\n", "").strip()

t1 = []
t2 = []
with open(sys.argv[1], "r", encoding="utf-8") as fd:
    while True:
        line = list(islice(fd, 3))
        if not line:
            break
        l1 = formatLine(line[0])
        l2 = formatLine(line[1])
        if l1 != "":
            t1.append(l1)
        if l2 != "":
            t2.append(l2)
with open("fixed.txt", "w", encoding="utf-8") as fd:
    for i in range(0, len(t1)):
        if i < len(t2):
            fd.write(f"{t1[i]}\n")
            fd.write(f"{t2[i]}\n")
            fd.write("----------------\n")