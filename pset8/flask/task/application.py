from flask import Flask, redirect, render_template, request

app = Flask(__name__)

todos = [] #Global variable

@app.route("/")
def tasks():
    return render_template("tasks.html", todos = todos) #passing the updated todo list to my tasks page

@app.route("/add", methods = ["GET", "POST"]) #default is GET, this way we can have a POSt request too, someone submitted data from add to the server
def add():
    if request.method == "GET":
        return render_template("add.html") # that is a GET request
    else:
        todo = request.form.get("task")
        todos.append(todo)
        return redirect("/") #after task has been added redirect back to the main route

#GET is the request method to get information from a page
#POST send data to a particular route