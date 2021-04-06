import random

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    number = random.randint(1, 10)
    return render_template("index.html", number=number) #number on right is python value,which the value on line 9, number on left is variable, which the template accesses

@app.route("/goodbye")
def bye():
    return "Goodbye!"