from cs50 import SQL
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

db = SQL("sqlite:///lecture.db") # db gives me access to the db file, so i can run sql queries

@app.route("/")
def index():
    rows = db.execute("SELECT * FROM registrants") #run query to get DATA and store in rows
    return render_template("index.html", rows = rows)

@app.route("/register", methods =["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("name")
        if not name:
            return render_template("apology.html", message = "Name required")
        email = request.form.get("email")
        if not email:
            return render_template("apology.html", message = "Email required")
        db.execute("INSERT INTO registrants (name, email) VALUES (:name, :email)", name=name, email=email)
        # :name and :email are placeholders, no sql attack !!
        return redirect("/")