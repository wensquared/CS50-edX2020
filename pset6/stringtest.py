from sys import argv, exit
import csv


if len(argv) != 3:

    print("missing files, need cvs file and dna seq textfile")
    exit(1)

f = open(argv[1])
seq = f.read()
dna = argv[2]

index = []

for i in range(len(seq)):
    s = seq.find(dna, i, i + len(dna))

    if s != -1:
        index.append(s)

print(index)
temp = 1
c = 1

for i in range(len(index)-1):
    s = index[i+1] - index[i]
    if s == len(dna):
        temp += 1
        if temp >= c:
            c = temp
    else:
        temp = 1

print(c)