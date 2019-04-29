import base64
import io
from imageio import imread, imwrite
from PIL import ImageTk, Image
import numpy as np
import logging

from skimage import data, img_as_float
from skimage import exposure
from skimage import util

from flask_pymongo import PyMongo
from flask import Flask, request, jsonify, abort
from my_class import User
from pymodm import connect
import datetime
import matplotlib
matplotlib.use('TkAgg')

app = Flask(__name__)

connect("mongodb+srv://mlw60:Wm347609@bme547-r5nv9."
        "mongodb.net/test?retryWrites=true")

app.config['MONGO_DBNAME'] = "bme547"
app.config['MONGO_URI'] = "mongodb+srv://mlw60:Wm347609@bme547-r5nv9." \
                          "mongodb.net/test?retryWrites=true"

mongo = PyMongo(app)

Error = {
        1: {"message": "Please enter a username in the designated entry bar."},
            }

logging.basicConfig(filename="Main.log", filemode="w", level=logging.INFO)


@app.route("/", methods=["GET"])
def server_on():
    """Checks if server is on
    """
    logging.info('Server on!')
    return "Image Processing Server On"


@app.route("/user_name", methods=["POST"])
def user_name():
    """Saves the username and time uploaded to MongoDB
    Receives a dictionary containing the user's
    username, and calls upload_time and add_user_name
    to save the user's information to the database

    Returns:
        str: reports that it added the username
    """
    r = request.get_json()
    user_name = r["user_name"]
    time = upload_time()

    try:
        add_user_name(user_name, time)
        logging.info('Username saved successfully!')
    except errors.ValidationError:
        logging.warning(Error[1])
        return jsonify(Error[1]), 500
    return "Added user name!", 200


def upload_time():
    """Finds and saves the current timestamp

    Returns:
        time (datetime string): current time
    """
    time = datetime.datetime.now()
    return time


def add_user_name(user_name_arg, time):
    """Saves the username and time uploaded to MongoDB database

    Args:
        user_name_arg (string): user-specified username to identify
            each unique user
        time (datetime string): the time the image(s) were
            uploaded
    """
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
    add_raw_image(user_name, raw_b64_strings)
    imgs_io = image_decode(user_name, raw_b64_strings)
    img_procs = image_processing(imgs_io, processing_type)
    proc_b64_strings = processed_image(user_name, img_procs)
    time2 = datetime.datetime.now()
    time_to_process = time2 - time1
    add_time_to_process(time_to_process, user_name)

    return "Added user's image processing type preference!", 200


def add_processing_type(user_name_arg, processing_type_arg):
    """Saves the processing type to MongoDB database under the
    corresponding username

    Args:
        user_name_arg (str): user-specified username to identify
            each unique user
        processing_type_arg (str): user-specified processing type
            for the images
    """
    u = User.objects.raw({"_id": user_name_arg}).first()
    u.processing_type = processing_type_arg
    u.save()


def add_raw_image(user_name_arg, raw_b64_strings):
    """Saves the raw image(s) in the form of b64 string(s)
    to MongoDB database under the corresponding username

    Args:
        user_name_arg (str): user-specified username to identify
            each unique user
        raw_b64_strings (str): b64 strings of the images uplaoded
            by the user before image processing
    """
    u = User.objects.raw({"_id": user_name_arg}).first()
    u.original_image = raw_b64_strings
    u.save()


def image_decode(user_name_arg, raw_b64_strings):
    """Converts the b64 strings of the raw uploaded images into bytes
    and then converted into imageio.core.util.Array objects that are a
    subclass of np.ndarray with a meta attribute. JPEG images of these raw
    objects are created in this function to check the functionality
    of the server

    Args:
        user_name_arg (str): user-specified username to identify
            each unique user
        raw_b64_strings (str): b64 strings of the images uplaoded
            by the user before image processing

    Returns:
        list: list of numpy-like objects of the images uplaoded
            by the user before image processing
    """
    import matplotlib.pyplot as plt
    imgs_io = []

    for i in range(len(raw_b64_strings)):
        image_bytes = base64.b64decode(raw_b64_strings[i])
        img_io = imread(io.BytesIO(image_bytes))
        imgs_io.append(img_io)
        plt.imsave('raw_test_{}.jpg'.format(i), img_io)
    return imgs_io


def image_processing(imgs_io, processing_type):
    """Converts the list of imageio.core.util.Array objects into numpy
    arrays and then carries out the image processing step, returning
    a list of numpy arrays after image processing. JPEG images of these
    processed arrays are created in this function to check the
    functionality of the server

    Args:
        imgs_io (list): list of numpy-like objects of the images uplaoded
            by the user before image processing
        processing_type (str): user-specified processing type
            for the images

    Returns:
        list: list of numpy arrays of the images after image processing
    """
    import matplotlib.pyplot as plt
    img_procs = []

    for i in range(len(imgs_io)):
        img = np.asarray(imgs_io[i].astype('uint8'))
        if processing_type == 'hist_eq':
            img_proc = hist_equalization(img)
        elif processing_type == 'con_stretch':
            img_proc = contrast_stretching(img)
        elif processing_type == 'log_comp':
            img_proc = log_compression(img)
        elif processing_type == 'reverse_vid':
            img_proc = reverse_video(img)
        img_procs.append(img_proc)
        plt.imsave('proc_test_{}.jpg'.format(i), img_proc)
    return img_procs


def hist_equalization(img):
    """Performs histogram equalization processing on raw image

    Args:
        img (np array): raw image in the form of a np array

    Returns:
        np array: image array after having histogram equalization
            performed
    """
    img_eq = exposure.equalize_hist(img)
    logging.info('Histogram equalization performed!')
    return img_eq


def contrast_stretching(img):
    """Performs contrast stretching processing on raw image

    Args:
        img (np array): raw image in the form of a np array

    Returns:
        np array: image array after having contrast stretching
            performed
    """
    p2, p98 = np.percentile(img, (2, 98))
    img_con = exposure.rescale_intensity(img, in_range=(p2, p98))
    logging.info('Contrast stretching performed!')
    return img_con


def log_compression(img):
    """Performs log compression processing on raw image

    Args:
        img (np array): raw image in the form of a np array

    Returns:
        np array: image array after having log compression
            performed
    """
    img_log = exposure.adjust_log(img, 1)
    logging.info('Log compression performed!')
    return img_log


def reverse_video(img):
    """Performs reverse video processing on raw image

    Args:
        img (np array): raw image in the form of a np array

    Returns:
        np array: image array after having log compression
            performed
    """
    img_inv = util.invert(img, signed_float=False)
    logging.info('Reverse video performed!')
    return img_inv


def processed_image(user_name, img_procs):
    """Converts list of numpy arrays of processed images into
    b64 strings that are saved to the MongoDB database

    Args:
        user_name (str): user-specified username to identify
            each unique user
        imgs_procs (list): list of numpy arrays of the images
            after image processing

    Returns:
        list: list of b64 strings of the images uploaded by the
        user after image processing with the specified processing method
    """
    proc_b64_strings = []

    for i in range(len(img_procs)):
        pil_img = Image.fromarray(img_procs[i].astype('uint8'))
        pil_img_RGB = pil_img.convert('RGB')
        buff = io.BytesIO()
        pil_img_RGB.save(buff, format="JPEG")
        proc_b64_string = base64.b64encode(buff.getvalue()).decode("utf-8")
        proc_b64_strings.append(proc_b64_string)

    add_proc_image(user_name, proc_b64_strings)
    return proc_b64_strings


def add_proc_image(user_name_arg, proc_b64_strings):
    """Saves the processed image(s) in the form of b64 string(s)
    to MongoDB database under the corresponding username

    Args:
        user_name_arg (str): user-specified username to identify
            each unique user
        proc_b64_strings (str): list of b64 strings of the images
            uploaded by the user after image processing with the
            specified processing method
    """
    u = User.objects.raw({"_id": user_name_arg}).first()
    u.processed_image = proc_b64_strings
    u.save()


def add_time_to_process(time_to_process_arg, user_name_arg):
    """Saves the amount of elapsed time the server took to
    process the image(s) to MongoDB database under the corresponding
    username

    Args:
        user_name_arg (str): user-specified username to identify
            each unique user
        time_to_process_arg (datetime str): the amount of time
            the server took to process the image(s)
    """
    u = User.objects.raw({"_id": user_name_arg}).first()
    u.time_to_process = time_to_process_arg
    u.save()


@app.route("/time_metadata/<username>", methods=["GET"])
def get_time_stamp(username):
    """Gets the time uploaded and processing time from the
    database

    Args:
        username (str): user-specified username to identify
            each unique user

    Returns:
        dict: a dict of time uploaded and process time
    """
    for user in User.objects.raw({}):
        if user.user_name == username:
            time_stamp = {"time_uploaded": user.time_uploaded,
                          "process_time": user.time_to_process}
            return jsonify(time_stamp), 200


@app.route("/processed_image/<username>", methods=["GET"])
def get_proc_image(username):
    """Gets the processed image b64 string from the database

    Args:
        username (str): user-specified username to identify
            each unique user

    Returns:
        dict: a dict of the processed image in the form of a b64 string
    """
    for user in User.objects.raw({}):
        if user.user_name == username:
            image_output = {"processed_images": user.processed_image
                            }
            return jsonify(image_output), 200


if __name__ == '__main__':
    app.run()
