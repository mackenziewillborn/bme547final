from flask_pymongo import PyMongo
from flask import Flask, request
from my_class import User
import datetime
from pymodm import connect

app = Flask(__name__)

connect("mongodb+srv://mlw60:Wm347609@bme547-r5nv9.mongodb.net/test?retryWrites=true")

app.config['MONGO_DBNAME'] = "bme547"
app.config['MONGO_URI'] = "mongodb+srv://mlw60:Wm347609@bme547-r5nv9.mongodb.net/test?retryWrites=true"

mongo = PyMongo(app)


def add_new_user(user_name_arg, processing_type_arg, time_uploaded_arg, time_to_process_arg, image_size_arg):
    u = User(user_name=user_name_arg,
             processing_type=processing_type_arg,
             time_uploaded=time_uploaded_arg,
             time_to_process=time_to_process_arg,
             image_size=image_size_arg,
             )
    u.save()


def add_user_name(user_name_arg):
    u = User(user_name=user_name_arg)
    u.save()


def add_processing_type(user_name_arg, processing_type_arg, image_display_arg):
    u = User(user_name=user_name_arg,
             processing_type=processing_type_arg,
             image_display=image_display_arg)
    u.save()


def upload_time():
    time_stamp = datetime.datetime.now()
    return time_stamp


@app.route("/user_name", methods=["POST"])
def user_name():
    r = request.get_json()
    user_name = r["user_name"]
    add_user_name(user_name)
    return "Added user name!"


@app.route("/User")
def add():
    time_stamp = upload_time
    add_new_user("katie40", "brighter", time_stamp, "70 seconds", 60)
    return "Added user!"


@app.route("/processing_type", methods=["POST"])
def processing_type():
    r = request.get_json()
    user_name = r["user_name"]
    processing_type = r["processing_type"]
    image_display = r["image_display"]
    add_processing_type(user_name, processing_type, image_display)
    return "Added user's image processing type and image display preference!"


if __name__ == '__main__':
    app.run()

