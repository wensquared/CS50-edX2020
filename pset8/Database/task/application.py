from flask import Flask, redirect, render_template, request, session
from flask_session import Session

app = Flask(__name__)

#todos = [] #Global variable, but we want to store different data for different users, and not all users use the same data
#, for example email,so we do it through sessions, see below

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem" #the location where I want to store all data pertaining to sessions is going to be any
#file system of the web server that I'm running this application from, which in this case is CS50 IDE

Session(app) #to enable session for this particular flask web application

#which means I have access to a python dictionary - collection of key value pairs - called session where I can access information
#that is going to be local to the user's current interaction with the web page

@app.route("/")
def tasks():
    if "todos" not in session:
        session["todos"] = []  #for the current user do they alerady have a key called todos inside the current user's session dictionary
        #if they dont, then we're going to create a new key inside of the session dict called todos and set it equel to empty list
    return render_template("tasks.html", todos = session["todos"]) #passing the updated todo list to my tasks page

@app.route("/add", methods = ["GET", "POST"]) #default is GET, this way we can have a POSt request too, someone submitted data from add to the server
def add():
    if request.method == "GET":
        return render_template("add.html") # that is a GET request
    else:
        todo = request.form.get("task")
        session["todos"].append(todo)
        return redirect("/") #after task has been added redirect back to the main route

#GET is the request method to get information from a page
#POST send data to a particular route