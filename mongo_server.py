from flask_pymongo import PyMongo
from flask import Flask, request
from my_class import User
import datetime
from pymodm import connect
# import matplotlib
# import matplotlib.pyplot as plt
# import numpy as np
# from skimage import data, img_as_float
# from skimage import exposure

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


# def add_processing_type(user_name_arg, processing_type_arg):
#     u = User(user_name=user_name_arg,
#              processing_type=processing_type_arg)
#     u.save()


def upload_time():
    time_stamp = datetime.datetime.now()
    return time_stamp


@app.route("/user_name", methods=["POST"])
def user_name():
    r = request.get_json()
    add_user_name(r)
    return "Added user name!"


@app.route("/User")
def add():
    time_stamp = upload_time
    add_new_user("katie40", "brighter", time_stamp, "70 seconds", 60)
    return "Added user!"


# @app.route("/Image")
# def image():
#     img = data.camera()
#     plt.figure(figsize=(4, 4))
#     plt.imshow(img, cmap='gray')
#     plt.axis("off")
#     plt.show()


if __name__ == '__main__':
    app.run()
