from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", name="Emma") #render_template can pass also variables to our html file: giving index.html access to variable called name

@app.route("/goodbye")
def bye():
    return "Goodbye!"