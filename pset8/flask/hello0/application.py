from flask import Flask

app = Flask(__name__) #app..variable to represent flask application, name...serving this flask application from this file that i'm writing right now

@app.route("/") #routes...name of url, page u want to visit, /...default route
def index(): #every route has function
    return "<h1>Hello, world!</h1>"

@app.route("/goodbye") #if u type in above url line at the end /goodbye
def bye():
    return "Goodbye!"
