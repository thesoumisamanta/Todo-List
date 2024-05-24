from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timezone

app = Flask(__name__)

# MongoDB configuration
client = MongoClient("mongodb://localhost:27017/")
db = client["todo_db"]
todos_collection = db["todos"]

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':  
        title = request.form['title']
        desc = request.form['desc']
        date_created = datetime.now(timezone.utc)

        todo = {
            "title": title,
            "desc": desc,
            "date_created": date_created
        }
        todos_collection.insert_one(todo)

    all_todos = list(todos_collection.find())
    return render_template('index.html', allTodo=all_todos)


@app.route('/show')
def product():
    all_todos = list(todos_collection.find())
    print(all_todos)
    return 'Wow, This is Amazing!'

@app.route('/update/<string:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        todos_collection.update_one(
            {"_id": ObjectId(sno)},
            {"$set": {"title": title, "desc": desc}}
        )
        return redirect("/")

    todo = todos_collection.find_one({"_id": ObjectId(sno)})
    return render_template('update.html', todo=todo)

@app.route('/delete/<string:sno>')
def delete(sno):
    todos_collection.delete_one({"_id": ObjectId(sno)})
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
