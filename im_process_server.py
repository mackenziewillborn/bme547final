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
from flask import Flask, request, jsonify, abort
from my_class import User
from pymodm import connect
import datetime

app = Flask(__name__)

connect("mongodb+srv://mlw60:Wm347609@bme547-r5nv9."
        "mongodb.net/test?retryWrites=true")

app.config['MONGO_DBNAME'] = "bme547"
app.config['MONGO_URI'] = "mongodb+srv://mlw60:Wm347609@bme547-r5nv9." \
                          "mongodb.net/test?retryWrites=true"

mongo = PyMongo(app)


@app.route("/", methods=["GET"])
def server_on():
    return "Image Processing Server On"


@app.route("/user_name", methods=["POST"])
def user_name():
    r = request.get_json()
    user_name = r["user_name"]
    time = upload_time()
    add_user_name(user_name, time)
    return "Added user name!"


def upload_time():
    time = datetime.datetime.now()
    return time


def add_user_name(user_name_arg, time):
    u = User(user_name=user_name_arg,
             time_uploaded=time)
    u.save()


@app.route("/processing_type", methods=["POST"])
def processing_type():
    r = request.get_json()
    user_name = r["user_name"]
    raw_b64_strings = r["raw_b64_strings"]
    processing_type = r["processing_type"]

    add_processing_type(user_name, processing_type)
    time1 = datetime.datetime.now()
    img_io = image_decode(user_name, raw_b64_strings)
    add_raw_image(user_name, raw_b64_strings)
    img_proc = image_processing(img_io, processing_type)
    proc_b64_string = processed_image(user_name, img_proc)
    time2 = datetime.datetime.now()
    time_to_process = time2 - time1
    add_time_to_process(time_to_process, user_name)

    return "Added user's image processing type preference!"


def add_processing_type(user_name_arg, processing_type_arg):
    u = User.objects.raw({"_id": user_name_arg}).first()
    u.processing_type = processing_type_arg
    u.save()


def image_decode(user_name_arg, raw_b64_strings):
    for i in range(len(raw_b64_strings)):
        image_bytes = base64.b64decode(raw_b64_strings[i])
        img_io = imread(io.BytesIO(image_bytes))
        plt.imsave('raw_test_{}.jpg'.format(i), img_io)
    return img_io


def add_raw_image(user_name_arg, raw_b64_strings):
    u = User.objects.raw({"_id": user_name_arg}).first()
    u.original_image = raw_b64_strings
    u.save()


def image_processing(img_io, processing_type):
    img = np.asarray(img_io.astype('uint8'))
    if processing_type == 'hist_eq':
        img_proc = hist_equalization(img)
    elif processing_type == 'con_stretch':
        img_proc = contrast_stretching(img)
    elif processing_type == 'log_comp':
        img_proc = log_compression(img)
    elif processing_type == 'reverse_vid':
        img_proc = reverse_video(img)
    # else:
    #     img_proc = hist_equalization(img)
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


def processed_image(user_name, img_proc):
    # proc_img_bytes = img_proc.tobytes()
    # proc_b64_bytes = base64.b64encode(proc_img_bytes)
    pil_img = Image.fromarray(img_proc.astype('uint8'))
    buff = io.BytesIO()
    pil_img.save(buff, format="JPEG")
    proc_b64_string = base64.b64encode(buff.getvalue()).decode("utf-8")

    # proc_b64_string = str(proc_b64_bytes, encoding='utf-8')
    add_proc_image(user_name, proc_b64_string)
    return proc_b64_string


def add_proc_image(user_name_arg, proc_b64_string):
    u = User.objects.raw({"_id": user_name_arg}).first()
    u.processed_image = proc_b64_string
    u.save()


def add_time_to_process(time_to_process_arg, user_name_arg):
    u = User.objects.raw({"_id": user_name_arg}).first()
    u.time_to_process = time_to_process_arg
    u.save()


@app.route("/time_metadata/<username>", methods=["GET"])
def get_time_stamp(username):
    for user in User.objects.raw({}):
        if user.user_name == username:
            time_stamp = {"time_uploaded": user.time_uploaded,
                          "process_time": user.time_to_process}
            return jsonify(time_stamp)


@app.route("/processed_image/<username>", methods=["GET"])
def get_proc_image(username):
    for user in User.objects.raw({}):
        if user.user_name == username:
            image_output = {"processed_image": user.processed_image
                            }
            return jsonify(image_output)

if __name__ == '__main__':
    app.run()
