# TODO
import sys
import cs50
import csv 

def main():
    if len(sys.argv) != 2:
        print("Missing CSV file")
        exit(1)
    
    db = cs50.SQL("sqlite:///students.db")
    
    with open(sys.argv[1], "r") as students:
        reader = csv.DictReader(students)
        
        for row in reader:
            #print(row)
            name = row["name"].split()
            
            if len(name) <= 2:
                name.insert(1, None)
            #print(name)
            
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?,?,?,?,?)", name[0],name[1],name[2],row["house"],int(row["birth"]))
            

main()