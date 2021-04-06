from sys import argv, exit
import csv

if len(argv) != 3:

    print("missing files, need cvs file and dna seq textfile")
    exit(1)

f = open(argv[1])
dna = argv[2]

seq = f.read()

if seq[0:4] == dna:
    print("found")

print(seq)