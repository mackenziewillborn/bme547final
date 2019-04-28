from my_class import User
import datetime
from pymodm import connect

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

# test_image_decode
# test_image_processing
# test_hist_equalization
# test_contrast_stretching
# test_log_compression
# test_reverse_video
# test_processed_image
