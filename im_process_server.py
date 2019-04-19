from flask_pymongo import PyMongo
from flask import Flask, request
from my_class import User
from pymodm import connect

app = Flask(__name__)

connect("mongodb+srv://mlw60:Wm347609@bme547-r5nv9."
        "mongodb.net/test?retryWrites=true")

app.config['MONGO_DBNAME'] = "bme547"
app.config['MONGO_URI'] = "mongodb+srv://mlw60:Wm347609@bme547-r5nv9." \
                          "mongodb.net/test?retryWrites=true"

mongo = PyMongo(app)


def add_user_name(user_name_arg):
    u = User(user_name=user_name_arg)
    u.save()


@app.route("/user_name", methods=["POST"])
def user_name():
    r = request.get_json()
    user_name = r["user_name"]
    add_user_name(user_name)
    return "Added user name!"


if __name__ == '__main__':
    app.run()


