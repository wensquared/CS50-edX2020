#this is just a program to create data for the main project

from cs50 import SQL
import random
import string
from werkzeug.security import check_password_hash, generate_password_hash

db = SQL("sqlite:///guests.db")

# creating password for the invitation
# randomizes letters and numbers of a given length
def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    hash = generate_password_hash(result_str)
    return (result_str, hash)

#one time uses, only to create a guestlist to use in project

# 1.

#students.db from pset7, in sqlite minimzed it to the top20 and then inserted first and lastname it into table guestpw
#creating also generic username: 'guest+number' for the invitation

#username = 'guest'
#students = db.execute('SELECT * FROM students')
#j=1
#for student in students:
#    n = get_random_alphanumeric_string(6)
#    username = username+str(j)
#    db.execute('INSERT INTO guestspw (username, password, hash, firstname, lastname) VALUES (:username,:password,:hash,:firstname,:lastname)',
#                username=username, password=n[0],hash=n[1],firstname=student['first'],lastname=student['last'])
#    j=j+1
#    username = 'guest'


#2.

#created table guest, table, plusone, maxpeople (used in the final project) and initializing it

#guestspw = db.execute('SELECT * FROM guestspw')

#for guest in guestspw:
#    n=random.randint(1,3)
#    db.execute('INSERT INTO guests (username, hash, firstname, lastname, apetizer, maincourse, tablenum, comment, maxinvite) VALUES
#    (:username,:hash,:firstname,:lastname,:apetizer, :maincourse, :tablenum, :comment, :maxinvite)',
#   username=guest['username'],hash=guest['hash'],firstname=guest['firstname'],lastname=guest['lastname'],apetizer=0,maincourse=0,tablenum=0,comment='No comment',maxinvite=n)

#for i in range(1,9):
#    db.execute('INSERT INTO maxpeople (tablenum,maximum) VALUES (:tablenum,:maximum)',tablenum=i,maximum=10)
#    db.execute('INSERT INTO tables (maxpeople) VALUES (:maxpeople)',maxpeople=10)
