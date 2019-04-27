import base64
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import io
from imageio import imread, imwrite
from PIL import ImageTk, Image
import numpy as np

from skimage import data, img_as_float
from skimage import exposure
from skimage import util

import logging
from flask_pymongo import PyMongo
from flask import Flask, request, jsonify
from my_class import User
from pymodm import connect, errors
import datetime

app = Flask(__name__)

connect("mongodb+srv://mlw60:Wm347609@bme547-r5nv9."
        "mongodb.net/test?retryWrites=true")

app.config['MONGO_DBNAME'] = "bme547"
app.config['MONGO_URI'] = "mongodb+srv://mlw60:Wm347609@bme547-r5nv9." \
                          "mongodb.net/test?retryWrites=true"

mongo = PyMongo(app)


Error = {1: {"message": "The required Key was not entered."}}


def upload_time():
    time = datetime.datetime.now()
    return time


def add_user_name(user_name_arg, time):
    u = User(user_name=user_name_arg,
             time_uploaded=time)
    u.save()


def add_processing_type(user_name_arg, processing_type_arg):
    u = User.objects.raw({"_id": user_name_arg}).first()
    u.processing_type = processing_type_arg
    u.save()


def add_time_to_process(time_to_process_arg, user_name_arg):
    u = User.objects.raw({"_id": user_name_arg}).first()
    u.time_to_process = time_to_process_arg
    u.save()


def image_decode(user_name_arg, raw_b64_string):
    image_bytes = base64.b64decode(raw_b64_string)
    img_io = imread(io.BytesIO(image_bytes))
    plt.imsave('raw_test.jpg', img_io)
    # with open('new-img.jpg', 'wb') as raw_img:
    #     raw_img.write(image_bytes)
    return img_io


def add_raw_image(user_name_arg, raw_b64_string):
    u = User.objects.raw({"_id": user_name_arg}).first()
    u.original_image = raw_b64_string
    u.save()


def image_processing(img_io, processing_type):
    img = np.asarray(img_io)
    if processing_type == 'hist_eq':
        img_proc = hist_equalization(img)
    elif processing_type == 'con_stretch':
        img_proc = contrast_stretching(img)
    elif processing_type == 'log_comp':
        img_proc = log_compression(img)
    elif processing_type == 'reverse_vid':
        img_proc = reverse_video(img)
    else:
        img_proc = hist_equalization(img)
    plt.imsave('proc_test.jpg', img_proc)
    return img_proc


def hist_equalization(img):
    img_eq = exposure.equalize_hist(img)
    return img_eq


def contrast_stretching(img):
    p2, p98 = np.percentile(img, (2, 98))
    img_con = exposure.rescale_intensity(img, in_range=(p2, p98))
    return img_con


def log_compression(img):
    img_log = exposure.adjust_log(img, 1)
    return img_log


def reverse_video(img):
    img_inv = util.invert(img, signed_float=False)
    return img_inv


@app.route("/user_name", methods=["POST"])
def user_name():
    r = request.get_json()
    user_name = r["user_name"]
    time = upload_time()

    try:
        add_user_name(user_name, time)
    except errors.ValidationError:
        logging.warning(Error[1])
        return jsonify(Error[1]), 500
    except KeyError:
        logging.warning(Error[1])
        return jsonify(Error[1]), 500

    return "Added user name!"


@app.route("/processing_type", methods=["POST"])
def processing_type():
    r = request.get_json()

    user_name = r["user_name"]
    raw_b64_string = r["raw_b64_string"]
    processing_type = r["processing_type"]

    add_processing_type(user_name, processing_type)
    time1 = datetime.datetime.now()
    img_io = image_decode(user_name, raw_b64_string)
    add_raw_image(user_name, raw_b64_string)
    img_proc = image_processing(img_io, processing_type)
    proc_b64_string = processed_image(user_name, img_proc)
    time2 = datetime.datetime.now()
    time_to_process = time2 - time1
    add_time_to_process(time_to_process, user_name)

    return "Added user's image processing type preference!"


@app.route("/processed_image", methods=["POST"])
def post_upload_time():
    for user in User.objects.raw({}):
        print(user.user_name)
    return


def processed_image(user_name, img_proc):
    proc_img_bytes = img_proc.tobytes()
    proc_b64_bytes = base64.b64encode(proc_img_bytes)
    proc_b64_string = str(proc_b64_bytes, encoding='utf-8')
    add_proc_image(user_name, proc_b64_string)
    return proc_b64_string


def add_proc_image(user_name_arg, proc_b64_string):
    u = User.objects.raw({"_id": user_name_arg}).first()
    u.processed_image = proc_b64_string
    u.save()


@app.route("/processed_image", methods=["GET"])
def send_proc_image(proc_b64_string):
    image_output = {"processed_image": proc_b64_string
                    }
    return jsonify(image_output)


if __name__ == '__main__':
    app.run()
