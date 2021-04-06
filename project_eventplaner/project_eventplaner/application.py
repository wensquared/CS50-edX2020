import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///guests.db")


@app.route("/")
@login_required
def index():
    """Show overview"""

    mainguest = db.execute("SELECT * FROM guests WHERE id=:user_id", user_id=session["user_id"])
    firstname = mainguest[0]["firstname"]
    lastname = mainguest[0]['lastname']

    plusone = db.execute("SELECT * FROM plusone WHERE relid=:user_id", user_id=session["user_id"])
    return render_template("index.html",mainguest=mainguest,plusone=plusone)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM guests WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/changelogin", methods=["GET", "POST"])
@login_required
def changelogin():
    """guest can change their login details"""

    if request.method == "GET":
        data = db.execute("SELECT username FROM guests WHERE id=:user_id", user_id=session["user_id"])
        return render_template("changelogin.html",oldusername = data[0]["username"])
    else:
        #getting new username and password from user
        if not request.form.get("username"):
            return apology("Need a username",401)

        if not request.form.get('password'):
            return apology("Need a password",401)

        if not request.form.get("confpassword"):
            return apology("Please confirm password",401)

        # generating hash and checking if password hash and confirmed password hash is the same
        hashpw = generate_password_hash(request.form.get('password'))
        hashconfpw = generate_password_hash(request.form.get('confpassword'))

        if not request.form.get('password') == request.form.get('confpassword'):
            return apology("Password and confirmed password are not the same",401)

        #updating table
        db.execute("UPDATE guests SET username= :username, hash = :newhash WHERE id = :user_id",username=request.form.get("username"),newhash=hashpw, user_id=session['user_id'])

        return redirect('/')


@app.route("/addguest", methods=["GET", "POST"])
@login_required

def addguest():
    """mainguest can add companions"""
    if request.method == 'GET':
        return render_template('addguest.html')

    else:
        #getting first and last name of the companion
        firstname = db.execute('SELECT firstname FROM plusone')
        if not request.form.get('firstname'):
            return apology("Please provide a first name", 405)

        for name in firstname:
            if name['firstname'] == request.form.get('firstname'):
                return apology("Firstname already taken. Pls add number to the name", 405)

        if not request.form.get('lastname'):
            return apology("Please provide a last name", 405)

        #checking if main guest can add another person else error message appears
        invitees = db.execute('SELECT COUNT(relid) as invitees FROM plusone WHERE relid=:user_id',user_id=session['user_id'])
        maxinv=db.execute("SELECT maxinvite FROM guests WHERE id=:user_id",user_id=session['user_id'])
        if maxinv[0]['maxinvite'] == invitees[0]['invitees']:
            return apology('You already invited enough people.',405)

        # adding companion into table plusone (=companions table)
        db.execute("INSERT INTO plusone (firstname, lastname, relid, apetizer,maincourse,tablenum,comment) VALUES (:firstname, :lastname, :relid,:apetizer, :maincourse, :tablenum, :comment)",
                    firstname=request.form.get('firstname'), lastname=request.form.get('lastname'), relid=session["user_id"],apetizer=0, maincourse=0,tablenum=0, comment='No comment')

        return redirect("/")

@app.route("/removeguest", methods=["GET", "POST"])
@login_required

def removeguest():
    """mainguest can remove companion"""
    if request.method == 'GET':
        plusone = db.execute("SELECT * FROM plusone WHERE relid=:user_id", user_id=session["user_id"])
        return render_template("removeguest.html", plusone =plusone)

    #removing companion from every table in the database
    else:
        plusone = db.execute("SELECT * FROM plusone WHERE relid=:user_id", user_id=session["user_id"])
        idnumber = request.form.get('idnumber')
        removeguest = db.execute('SELECT * FROM plusone WHERE id=:idnumber',idnumber=idnumber)
        db.execute("DELETE FROM tables WHERE firstname=:firstname AND lastname=:lastname", firstname=removeguest[0]["firstname"],lastname=removeguest[0]["lastname"])
        db.execute("DELETE FROM plusone WHERE id=:idnumber",idnumber=idnumber)


        return redirect("/")

@app.route("/food", methods=["GET", "POST"])
@login_required

def food():
    """choose menu for each person"""
    guest = db.execute("SELECT * FROM guests WHERE id=:user_id",user_id=session['user_id'])
    plusone = db.execute("SELECT * FROM plusone WHERE relid=:user_id",user_id=session['user_id'])

    if request.method == 'GET':
        return render_template('food.html',guest=guest,plusone=plusone)

    else:
        firstname = request.form.get('firstname')
        apetizer = int(request.form.get('apetizer'))
        maincourse = int(request.form.get('main'))
        comment = request.form.get('comment')

        if firstname == guest[0]['firstname']:
            if not comment:
                db.execute('UPDATE guests SET apetizer=:apetizer, maincourse=:maincourse WHERE id=:user_id',apetizer=apetizer,maincourse=maincourse,user_id=session["user_id"])
            else:
                db.execute('UPDATE guests SET apetizer=:apetizer, maincourse=:maincourse, comment=:comment WHERE id=:user_id',apetizer=apetizer,maincourse=maincourse,comment=comment,user_id=session["user_id"])
        else:
            if not comment:
                db.execute('UPDATE plusone SET apetizer=:apetizer, maincourse=:maincourse WHERE firstname=:firstname',apetizer=apetizer,maincourse=maincourse,firstname=firstname)
            else:
                 db.execute('UPDATE plusone SET apetizer=:apetizer, maincourse=:maincourse, comment=:comment WHERE firstname=:firstname',apetizer=apetizer,maincourse=maincourse,comment=comment,firstname=firstname)

        return redirect("/")

@app.route("/table", methods=["GET", "POST"])
@login_required
def table():
    """choose table for each person"""
    guest = db.execute("SELECT * FROM guests WHERE id=:user_id",user_id=session['user_id'])
    plusone = db.execute("SELECT * FROM plusone WHERE relid=:user_id",user_id=session['user_id'])
    table = db.execute("SELECT * FROM tables")

    if request.method == 'GET':
        return render_template('table.html',guest=guest,plusone=plusone,table=table)

    else:
        firstname = request.form.get('firstname')
        tablenum = int(request.form.get('tablenum'))

        maxperson = db.execute('SELECT COUNT(tablenum) as maxp FROM tables WHERE tablenum=:tablenum',tablenum=tablenum)
        tablenumbermax  = db.execute('SELECT maximum FROM maxpeople WHERE tablenum=:tablenum',tablenum=tablenum)
        if maxperson[0]['maxp'] == tablenumbermax[0]['maximum']:
            return apology('Table already full',401)


        #adding main guest into table tables
        if firstname == guest[0]['firstname']:
            db.execute('UPDATE guests SET tablenum=:tablenum WHERE id=:user_id', tablenum=tablenum,user_id=session["user_id"])
            if guest[0]['tablenum'] == 0:
                db.execute('INSERT INTO tables (tablenum, firstname, lastname) VALUES (:tablenum, :firstname, :lastname)', tablenum=tablenum, firstname=guest[0]['firstname'],lastname=guest[0]['lastname'])
            else:
                db.execute('UPDATE tables SET tablenum=:tablenum WHERE firstname=:firstname',tablenum=tablenum, firstname=guest[0]['firstname'])
        #adding plusone into table tables
        else:
            theone = db.execute("SELECT * FROM plusone WHERE firstname=:firstname AND relid=:user_id", firstname=firstname, user_id=session['user_id'])
            db.execute('UPDATE plusone SET tablenum=:tablenum WHERE firstname=:firstname', tablenum=tablenum,firstname=theone[0]['firstname'])
            if theone[0]['tablenum'] == 0:
                db.execute('INSERT INTO tables (tablenum, firstname, lastname) VALUES (:tablenum, :firstname, :lastname)', tablenum=tablenum, firstname=theone[0]['firstname'],lastname=theone[0]['lastname'])
            else:
                db.execute('UPDATE tables SET tablenum=:tablenum WHERE firstname=:firstname',tablenum=tablenum, firstname=theone[0]['firstname'])

        return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
