# TODO
import cs50
import sys


if len(sys.argv) != 2:
    print("Missing word")
    exit(1)
        
db = cs50.SQL("sqlite:///students.db")

selected_list = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", sys.argv[1])

for row in selected_list:
    if row["middle"] != None:
        print(f'{row["first"]} {row["middle"]} {row["last"]}, born {row["birth"]}')
    else:
        print(f'{row["first"]} {row["last"]}, born {row["birth"]}')
    