import base64
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import io
from imageio import imread, imwrite
from PIL import ImageTk, Image
import numpy as np

from skimage import data, img_as_float
from skimage import exposure
from skimage import util

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


def add_processing_type(user_name_arg, processing_type_arg):
    u = User(user_name=user_name_arg,
             processing_type=processing_type_arg)
    u.save()


def image_decode(user_name_arg, raw_b64_string):
    image_bytes = base64.b64decode(raw_b64_string)
    img_io = imread(io.BytesIO(image_bytes))
    plt.imsave('raw_test.jpg', img_io)
    # u = User(user_name=user_name_arg,
    #              original_image=raw_img)
    # u.save()
    return img_io


@app.route("/user_name", methods=["POST"])
def user_name():
    r = request.get_json()
    user_name = r["user_name"]
    add_user_name(user_name)
    return "Added user name!"


@app.route("/processing_type", methods=["POST"])
def processing_type():
    r = request.get_json()
    user_name = r["user_name"]
    raw_b64_string = r["raw_b64_string"]
    processing_type = r["processing_type"]

    add_processing_type(user_name, processing_type)
    img_io = image_decode(user_name, raw_b64_string)
    return "Added user's image processing type preference!"


if __name__ == '__main__':
    app.run()
