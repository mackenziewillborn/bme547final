from my_class import User
import datetime
from pymodm import connect
import pytest
import numpy as np


connect("mongodb+srv://mlw60:Wm347609@bme547-r5nv9."
        "mongodb.net/test?retryWrites=true")


def test_add_user_name():
    from im_process_server import add_user_name

    username = "test user name"
    add_user_name(username, datetime.datetime.now())

    expected = User.objects.raw({"_id": username}).first()

    assert username == expected.user_name


def test_add_processing_type():
    from im_process_server import add_processing_type

    username = "test user name"
    processingtype = "test processing type"

    add_processing_type(username, processingtype)
    expected = User.objects.raw({"_id": username}).first()

    assert processingtype == expected.processing_type


def test_add_raw_image():
    from im_process_server import add_raw_image

    username = "test user name"
    rawb64string = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgc" \
                   "GBQgHBwcJCQgKDBQNDAsLDBkSEw8UHR..."

    add_raw_image(username, rawb64string)
    expected = User.objects.raw({"_id": username}).first()

    assert rawb64string == expected.original_image


def test_add_proc_image():
    from im_process_server import add_proc_image

    username = "test user name"
    procb64string = "SUkqAAgAAAAKAAABBAABAAAALAEAAAEBBAAB" \
                    "AAAAIAEAAAIBAwADAAAAhgAAAAMBAwABAA..."

    add_proc_image(username, procb64string)
    expected = User.objects.raw({"_id": username}).first()

    assert procb64string == expected.processed_image


def test_add_time_to_process():
    from im_process_server import add_time_to_process

    username = "test user name"
    timetoprocess = "0:00:00.644707"

    add_time_to_process(timetoprocess, username)
    expected = User.objects.raw({"_id": username}).first()

    assert timetoprocess == expected.time_to_process


def test_image_decode():
    from im_process_server import image_decode
    from testing_strings import rawb64images
    username = "test user name"

    decodedimg = image_decode(username, rawb64images)

    assert np.all(decodedimg[0:4, 1, 1] == [255, 255, 255, 255])


def test_hist_equalization():
    from im_process_server import hist_equalization
    from testing_strings import img

    img_eq = hist_equalization(img)
    img_eq_list = img_eq[0:4, 1, 0:4]
    expected = [[1., 1., 1., 0.18446181],
                [1., 1., 1., 0.18446181],
                [1., 1., 1., 0.18446181],
                [1., 1., 1., 0.18446181]]

    assert np.allclose(img_eq_list, np.array(expected))


def test_contrast_stretching():
    from im_process_server import contrast_stretching
    from testing_strings import img

    con_stretch = contrast_stretching(img)
    con_stretch_list = con_stretch[0:4, 1, 0:4]

    expected = [[255, 255, 255, 0],
                [255, 255, 255, 0],
                [255, 255, 255, 0],
                [255, 255, 255, 0]]

    assert np.all(con_stretch_list == np.array(expected))


def test_reverse_video():
    from im_process_server import reverse_video
    from testing_strings import img

    rev_vid = reverse_video(img)
    rev_vid_list = rev_vid[0:4, 1, 0:4]

    expected = [[0, 0, 0, 255],
                [0, 0, 0, 255],
                [0, 0, 0, 255],
                [0, 0, 0, 255]]

    assert np.all(rev_vid_list == np.array(expected))


def test_log_compression():
    from im_process_server import log_compression
    from testing_strings import img

    log_comp = log_compression(img)
    log_comp_list = log_comp[0:4, 1, 0:4]

    expected = [[255, 255, 255, 0],
                [255, 255, 255, 0],
                [255, 255, 255, 0],
                [255, 255, 255, 0]]

    assert np.all(log_comp_list == np.array(expected))
        
 
@pytest.mark.parametrize("processingtype, expected", [
    ("hist_eq", [[1., 1., 1., 0.18446181],
                 [1., 1., 1., 0.18446181],
                 [1., 1., 1., 0.18446181],
                 [1., 1., 1., 0.18446181]]),
    ("con_stretch", [[255, 255, 255, 0],
                     [255, 255, 255, 0],
                     [255, 255, 255, 0],
                     [255, 255, 255, 0]]),
    ("log_comp", [[255, 255, 255, 0],
                  [255, 255, 255, 0],
                  [255, 255, 255, 0],
                  [255, 255, 255, 0]]),
    ("reverse_vid", [[0, 0, 0, 255],
                     [0, 0, 0, 255],
                     [0, 0, 0, 255],
                     [0, 0, 0, 255]])])
def test_image_processing(processingtype, expected):
    from server_github import image_processing
    from testing_info import img

    improc = image_processing(img, processingtype)
    improc_list = improc[0:4, 1, 0:4]

    if processingtype == "hist_eq":
        assert np.allclose(improc_list, expected)
    else:
        assert np.all(improc_list == expected)
