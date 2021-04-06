from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html") # folder needs to be called templates, so we can call in the templates folder the file index.html//

@app.route("/goodbye")
def bye():
    return "Goodbye!"