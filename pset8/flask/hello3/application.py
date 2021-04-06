from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello")
def hello():
    name = request.args.get("name") #to access the value, what the user typed in in the name input field
    if not name: #if the name field is empty 
        return render_template("failure.html")
    return render_template("hello.html", name=name)