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

app = Flask(__name__)

connect("mongodb+srv://mlw60:Wm347609@bme547-r5nv9."
        "mongodb.net/test?retryWrites=true")

app.config['MONGO_DBNAME'] = "bme547"
app.config['MONGO_URI'] = "mongodb+srv://mlw60:Wm347609@bme547-r5nv9." \
                          "mongodb.net/test?retryWrites=true"

mongo = PyMongo(app)


@app.route("/user_name", methods=["POST"])
def user_name():
    r = request.get_json()
    user_name = r["user_name"]
    # add_user_name(user_name)
    return "Added user name!"


def add_user_name(user_name_arg):
    u = User(user_name=user_name_arg)
    u.save()


@app.route("/processing_type", methods=["POST"])
def processing_type():
    r = request.get_json()
    user_name = r["user_name"]
    raw_b64_string = r["raw_b64_string"]
    processing_type = r["processing_type"]

    # add_processing_type(user_name, processing_type)
    img_io = image_decode(user_name, processing_type, raw_b64_string)
    img_proc = image_processing(img_io, processing_type)
    # processed_image(user_name, img_proc)
    processed_image(img_proc)
    return "Added user's image processing type preference!"


def add_processing_type(user_name_arg, processing_type_arg):
    u = User(user_name=user_name_arg,
             processing_type=processing_type_arg)
    u.save()


def image_decode(user_name_arg, processing_type_arg, raw_b64_string):
    image_bytes = base64.b64decode(raw_b64_string)
    img_io = imread(io.BytesIO(image_bytes))
    plt.imsave('raw_test.jpg', img_io)
    # with open('new-img.jpg', 'wb') as raw_img:
    #     raw_img.write(image_bytes)
    # u = User(user_name=user_name_arg,
    #          processing_type=processing_type_arg,
    #          original_image=raw_b64_string)
    # u.save()
    return img_io


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


@app.route("/processed_image", methods=["GET"])
def processed_image(img_proc):
    proc_b64_string = add_processed_image(img_proc)
#     u = User(user_name=user_name_arg,
#              processed_image=proc_b64_string)
#     u.save()
    image_output = {"processed_image": proc_b64_string
                    }
    return jsonify(image_output)


def add_processed_image(img_proc):
    proc_img_bytes = img_proc.tobytes()
    proc_b64_bytes = base64.b64encode(proc_img_bytes)
    # buff = BytesIO()
    # pil_img.save(buff, format="JPEG")
    # proc_b64_string = base64.b64encode(buff.getvalue()).decode("utf-8")
    # with open(proc_img_jpg, "rb") as proc_image_file:
    #     proc_b64_bytes = base64.b64encode(proc_image_file.read())
    proc_b64_string = str(proc_b64_bytes, encoding='utf-8')
    return proc_b64_string

    # After the image is processed, I am going to save the processed image
    # into the database, encode the processed image
    # back to a base64 string, send it to the GUI as a GET request, and the
    # GUI will decode the string and display the processed image

if __name__ == '__main__':
    app.run()
