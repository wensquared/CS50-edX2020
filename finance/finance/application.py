import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    price_list={}
    total = 0

    users = db.execute("SELECT cash FROM users WHERE id=:user_id",user_id=session["user_id"])

    rows_buys = db.execute("SELECT symbol,SUM(shares) AS buy_shares,share_price FROM transactions WHERE user_id=:user_id GROUP BY symbol",user_id=session["user_id"])

    for stock in rows_buys:
        price_list[stock["symbol"]] = lookup(stock["symbol"])
        total = total + (stock["buy_shares"] * price_list[stock["symbol"]]["price"])

    total = total + users[0]["cash"]

    return render_template("index.html", stock_infos=rows_buys,cash=users, price_list=price_list,total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = lookup(request.form.get("symbol"))
        if symbol == None:
            return apology("This Stock doesn't exist.",300)

        price = symbol["price"]


        shares = int(request.form.get("shares"))
        amount = price*shares

        rows = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])
        balance = rows[0]["cash"]

        if amount > balance:
            return apology("Not enough money :'(",300)

        rest_cash = balance-amount

        db.execute("UPDATE users SET cash = :rest_cash WHERE id = :user_id", rest_cash=rest_cash, user_id=session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, share_price, status) VALUES (:user_id, :symbol, :shares, :share_price, :status)",user_id=session["user_id"], symbol=request.form.get("symbol"), shares=shares, share_price=price, status=1)

        return redirect("/")

@app.route("/addmoney", methods=["GET", "POST"])
@login_required
def addmoney():
    """Add money to balance sheet"""

    if request.method == "GET":
        return render_template("addmoney.html")
    else:
        add_money = request.form.get("add_money")

        db.execute("UPDATE users SET cash = cash + :amount WHERE id=:user_id",amount = add_money, user_id = session["user_id"])

        return redirect("/")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    transactions = db.execute("SELECT * from transactions WHERE user_id = :user_id ORDER BY created_at DESC", user_id=session["user_id"])
    return render_template("history.html", transactions=transactions)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        quote=lookup(request.form.get("quote"))

        if quote == None:
            return apology("No Symbol found",404)

        return render_template("quoted.html",quote=quote)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        if not username:
            return apology("Please provide a username",403)

        password = request.form.get("password")
        if not password:
            return apology("Please provide a password",403)

        confpassword = request.form.get("confpassword")
        if not confpassword:
            return apology("Please confirm your password",403)

        if not password == confpassword:
            return apology("Password and confirmed password doesn't match",403)

        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (:username,:hash)", username=username,hash=hash)

        #session["user_id"] = rows[0]["id"]

        return redirect("/login")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        return render_template("sell.html")
    else:
        symbol = lookup(request.form.get("symbol"))
        if symbol == None:
            return apology("This Stock doesn't exist.",300)

        price = symbol["price"]

        rows_sell = db.execute("SELECT SUM(shares) AS num_shares FROM transactions WHERE user_id=:user_id AND symbol=:symbol",user_id=session["user_id"],symbol=symbol["symbol"])

        shares = int(request.form.get("shares"))
        num_shares = rows_sell[0]["num_shares"]

        if shares > num_shares:
            return apology("You don't have that amount of shares left",200)

        amount = price*shares

        rows = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])
        balance = rows[0]["cash"]


        rest_cash = balance+amount

        db.execute("UPDATE users SET cash = :rest_cash WHERE id = :user_id", rest_cash=rest_cash, user_id=session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, share_price, status) VALUES (:user_id, :symbol, :shares, :share_price, :status)",
                    user_id=session["user_id"], symbol=request.form.get("symbol"), shares=(-shares), share_price=price, status=0)

        return redirect('/')


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
