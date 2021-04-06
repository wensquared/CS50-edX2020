from sys import argv, exit
import csv


def main():

    if len(argv) != 3:

        print("missing files, need cvs file and dna seq textfile")
        exit(1)

    #print("Read 2 files")

    database_file = csv.DictReader(open(argv[1]))
    f = open(argv[2])
    seq = f.read()

# Getting all STR in a list(dna_list)
    for row in database_file:
        # print(row)
        dna_list = list(row.keys())[1:]

    # print(dna_list)
    
# For each STR getting the longest repeat on a list(num)
    num = []
    
    for el in dna_list:
        num.append(find_high(el, seq))
    # print(num)
    
# Find the person with the exact dna sequence    
    winner = 'No match'
    
    database_file2 = csv.DictReader(open(argv[1]))
    length = len(dna_list)       
    for row in database_file2:
        j = 0
        for i in range(length):
            if int(row[dna_list[i]]) == num[i]:
                j += 1
                if j == length:
                    winner = row['name']
    
    print(winner)
    
    
def find_high(dna, seq):
    index = []

    for i in range(len(seq)):
        s = seq.find(dna, i, i + len(dna))

        if s != -1:
            index.append(s)

    # print(index)
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

    # print(c)
    return c

main()
