import base64
from tkinter import *
from tkinter import ttk
# from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
from tkinter import filedialog
import requests
from pymodm import connect
import cv2
import numpy as np
import io
from imageio import imread, imwrite
import matplotlib
matplotlib.use('TkAgg')

root = Tk()  # makes main window
root.title("GUI Client")
main_frame = Frame(root)
main_frame.pack()
URL = "http://127.0.0.1:5000"


def main():
    init_mongo_db()
    first_screen()


def init_mongo_db():
    """Initializes the connection to the database through mongoDB

    """
    connect("mongodb+srv://mlw60:Wm347609@bme547-r5nv9."
            "mongodb.net/test?retryWrites=true")


def first_screen():
    """The first screen of the GUI

    The first_screen function first asks the user to enter a
    username and saves that username as a string variable. It
    then has a button for the user to upload their raw image(s)
    to which they would like to perform image processing. The user
    can choose a single image, multiple images, or a zip file of
    images to upload. Then, the user clicks continue, which calls
    the continue function, which sends the username to the server
    and goes to the next screen of the GUI.

    """
    first_frame = Frame(root)
    first_frame.pack()
    top_label = ttk.Label(first_frame, text="Please enter a username below:")
    top_label.grid(column=0, row=0)

    username = StringVar()
    username_entry = ttk.Entry(first_frame, textvariable=username, width=20)
    username_entry.grid(column=0, row=1)

    browse_btn = ttk.Button(first_frame, text='Upload Raw Image(s)',
                            command=lambda: browse_function(first_frame))
    browse_btn.grid(column=0, row=2)

    ok_btn = ttk.Button(first_frame, text='Continue',
                        command=lambda: cont_function(username, first_frame))
    ok_btn.grid(column=1, row=3)

    root.mainloop()  # shows window


def browse_function(first_frame):
    """Creates a dialog box for the user to choose image files from
    their own local computer

    Allows the user to upload their raw image(s) to which they would
    like to perform image processing. The user can choose a single image,
    multiple images, or a zip file of images to upload.

    """
    global raw_filenames
    root.filename = \
        filedialog.askopenfilenames(initialdir="/", title="Select Image"
                                    )
    raw_filenames = root.filename
    num_files = len(raw_filenames)
    file_label = ttk.Label(first_frame,
                           text="{} file(s) uploaded".format(num_files))
    file_label.grid(column=0, row=3)


def cont_function(username, first_frame):
    """Posts username information to the server and proceeds
    to the next page of the GUI

    Args:
        username (tkinter.StringVar): user-specified username to identify
            each unique user
        first_frame (tkinter.Frame): frame of the first screen that is
            destroyed to move on to the second screen

    """
    new_user = {"user_name": username.get()
                }
    requests.post(URL+'/user_name', json=new_user)
    second_screen(username, first_frame)
    pass


def second_screen(username, first_frame):
    """The second screen of the GUI

    The second_screen function first destroys the first screen in order
    to display a new screen of the GUI. It asks the user to choose the
    image processing step they would like to user on their uploaded
    image(s). It saves the processing types as an IntVar for later
    use. It then provides a continue button that calls the process
    image function when clicked.

    Args:
        username ('tkinter.StringVar'): user-specified username to identify
            each unique user
        first_frame ('tkinter.Frame'): frame of the first screen that is
            destroyed to move on to the second screen

    Returns:
        tkinter.Frame: frame of the second screen that is destroyed
        to move on to the third GUI screen

    """
    first_frame.destroy()
    second_frame = Frame(root)
    second_frame.pack()

    top_label = ttk.Label(second_frame,
                          text="Select image processing step:",
                          font=("Helvetica", 20))
    top_label.grid(column=0, row=0)

    process_method = IntVar()
    ttk.Radiobutton(second_frame, text="Histogram Equalization",
                    variable=process_method,
                    value=1).grid(column=0, row=1, sticky=W)
    ttk.Radiobutton(second_frame, text="Contrast Stretching",
                    variable=process_method,
                    value=2).grid(column=0, row=2, sticky=W)
    ttk.Radiobutton(second_frame, text="Log Compression",
                    variable=process_method,
                    value=3).grid(column=0, row=3, sticky=W)
    ttk.Radiobutton(second_frame, text="Reverse Video",
                    variable=process_method,
                    value=4).grid(column=0, row=4, sticky=W)

    ok_btn = ttk.Button(second_frame, text='Continue',
                        command=lambda:
                        process_image(username, process_method, second_frame))
    ok_btn.grid(column=0, row=7)

    root.mainloop()  # shows window
    return second_frame


def process_image(username, process_method, second_frame):
    """Converts image to b64 string, parses the processing
    type variable, and sends information to server

    The process_image function first encodes the raw image and
    turns it into a b64 string. It then reads in the IntVar that
    was specifies previously by the user to determine which processing
    type the user chose. It finally send the username, raw b64 string,
    and specified processing type to the server and calls the third
    screen function to proceed to the next screen in the GUI.

    Args:
        username (tkinter.StringVar): user-specified username to identify
            each unique user
        process_method (tkinter.IntVar): a value of either 1, 2, 3, or 4
            that corresponds with histogram equalization, contrast stretching,
            log compression, or reverse video
        second_frame (tkinter.Frame): frame of the second screen that is
            destroyed to move on to the third GUI screen

    """
    raw_b64_strings = []

    for i in range(len(raw_filenames)):
        with open(raw_filenames[i], "rb") as raw_image_file:
            raw_b64_bytes = base64.b64encode(raw_image_file.read())
        raw_b64_string = str(raw_b64_bytes, encoding='utf-8')
        raw_b64_strings.append(raw_b64_string)
        if process_method.get() == 1:
            processing_type = 'hist_eq'
        elif process_method.get() == 2:
            processing_type = 'con_stretch'
        elif process_method.get() == 3:
            processing_type = 'log_comp'
        elif process_method.get() == 4:
            processing_type = 'reverse_vid'
        else:
            processing_type = 'hist_eq'

    user_processing_type = {"user_name": username.get(),
                            "raw_b64_strings": raw_b64_strings,
                            "processing_type": processing_type}
    requests.post(URL+'/processing_type', json=user_processing_type)
    third_screen(username, second_frame)
    return


def third_screen(username, second_frame):
    second_frame.destroy()
    third_frame = Frame(root)
    third_frame.pack()
    time_uploaded, process_time = get_time_metadata(username)

    ttk.Label(third_frame, text="Time Uploaded: {}".
              format(time_uploaded)).grid(column=0,
                                          row=0, columnspan=2, sticky=W)

    ttk.Label(third_frame, text="Time to Process: {}".
              format(process_time)).grid(column=0,
                                         row=1, columnspan=2, sticky=W)

    im_size = cv2.imread(raw_filenames[0], cv2.IMREAD_UNCHANGED)
    height = im_size.shape[0]
    width = im_size.shape[1]
    ttk.Label(third_frame, text="Image Size: {} x {} pixels".
              format(width, height)).grid(column=0, row=2,
                                          columnspan=2, sticky=W)

    display_btn = ttk.Button(third_frame,
                             text='Raw vs. Processed Images',
                             command=lambda: image_window(username))
    display_btn.grid(column=0, row=3)

    image_download = ttk.Label(third_frame,
                               text="Download processed image as:")
    image_download.grid(column=3, row=0,
                        rowspan=2, columnspan=2, sticky=W)

    image_format = StringVar()
    dropdown_menu = ttk.Combobox(third_frame, textvariable=image_format)
    dropdown_menu.grid(column=3, row=2, sticky=W)
    dropdown_menu['values'] = ('JPEG', 'PNG', 'TIFF')

    download_btn = ttk.Button(third_frame, text='Download',
                              command=lambda: download_function
                              (image_format, third_frame))
    download_btn.grid(column=4, row=6)
    reprocess_btn = ttk.Button(third_frame,
                               text='Apply another Processing Method',
                               command=lambda:
                               reprocess_function(username, third_frame))
    reprocess_btn.grid(column=3, row=6)

    root.mainloop()  # shows window
    return third_frame


def get_time_metadata(username):
    """Gets the time uploaded and processing time for the uploaded image(s)

    Args:
        username (tkinter.StringVar): user-specified username to identify
        each unique user

    Returns:
        str: the time that the image(s) were uploaded to the database
        str: the amount of time the server took to process the image(s)

    """
    r = requests.get(URL+'/time_metadata/'+username.get())
    r_json = r.json()
    time_uploaded = r_json['time_uploaded']
    process_time = r_json['process_time']
    return time_uploaded, process_time


def get_processed_image(username):
    """Gets the b64 string of the processed image from the server and
    converts it to an image file

    Args:
        username (tkinter.StringVar): user-specified username to identify
        each unique user

    Returns:
        JpegImageFile: the image file of the processed image

    """
    global proc_b64_string

    r = requests.get(URL+'/processed_image/'+username.get())
    r_json = r.json()
    proc_b64_string = r_json['processed_image']
    proc_image_bytes = base64.b64decode(proc_b64_string)
    plot_im = Image.open(io.BytesIO(proc_image_bytes))
    return plot_im


def image_window(username):
    """Displays the raw image and processed image side by side for
    comparison

    This function creates a new window to display both images. It uses
    the raw filepath to display the raw image, then calls the
    get_processed_image function in order to display the processed image.

    Args:
        username (tkinter.StringVar): user-specified username to identify
        each unique user

    """
    image_win = Toplevel(root)

    raw_open = Image.open(raw_filenames[-1])
    raw_image = ImageTk.PhotoImage(raw_open)

    plot_im = get_processed_image(username)
    photoimg = ImageTk.PhotoImage(plot_im)

    panel1 = Label(image_win, image=raw_image)
    panel1.grid(row=0, column=0)
    panel1 = Label(image_win, text="Raw Image")
    panel1.grid(row=1, column=0)

    panel2 = Label(image_win, image=photoimg)
    panel2.grid(row=0, column=1)
    panel1 = Label(image_win, text="Processed Image")
    panel1.grid(row=1, column=1)
    root.mainloop()


def download_function(image_format, third_frame):
    """Downloads the image(s) to the user's repository

    This function calls the get_processed_image function
    and creates a numpy array as an argument for the
    cv2.imwrite command, which saves the image as the specified
    filetype. It then moves on to the next page of the GUI that
    indicates that all images were successfully downloaded.

    Args:
        image_format(tkinter.StringVar): one of three options for the image
            filetype that will be downloaded, which are either JPEG, PNG,
            or TIFF
        third_frame: frame of the third screen that is destroyed
            to move on to the download GUI screen

    """
    import matplotlib.pyplot as plt
    proc_image_bytes = base64.b64decode(proc_b64_string)
    proc_im = imread(io.BytesIO(proc_image_bytes))

    if image_format.get() == 'JPEG':
        plt.imsave('processed.jpg', proc_im)
    elif image_format.get() == 'PNG':
        plt.imsave('processed.png', proc_im)
    elif image_format.get() == 'TIFF':
        plt.imsave('processed.tiff', proc_im)

    third_frame.destroy()
    download_frame = Frame(root)
    download_frame.pack()
    download_label = ttk.Label(download_frame,
                               text='All images downloaded successfully!',
                               font=("Helvetica", 25))
    download_label.grid(column=0, row=0)


def reprocess_function(username, third_frame):
    """Allows users to apply a new processing type to the same image(s)

    This function first destroys the third frame to display a new
    screen of the GUI. It allows the user to select another image
    processing step that is then applied to the same photos that
    were previously processed. The continue button calls the
    process_image function to process the images again.

    Args:
        username (tkinter.StringVar): user-specified username to identify
            each unique user
        third_frame (tkinter.Frame): frame of the third screen that is
            destroyed to move on to the reprocess GUI screen

    """
    # takes you back to the first screen
    third_frame.destroy()
    reprocess_frame = Frame(root)
    reprocess_frame.pack()

    top_label = ttk.Label(reprocess_frame,
                          text="Select next image processing step:",
                          font=("Helvetica", 20))
    top_label.grid(column=0, row=0)

    process_method = IntVar()
    ttk.Radiobutton(reprocess_frame, text="Histogram Equalization",
                    variable=process_method,
                    value=1).grid(column=0, row=1, sticky=W)
    ttk.Radiobutton(reprocess_frame, text="Contrast Stretching",
                    variable=process_method,
                    value=2).grid(column=0, row=2, sticky=W)
    ttk.Radiobutton(reprocess_frame, text="Log Compression",
                    variable=process_method,
                    value=3).grid(column=0, row=3, sticky=W)
    ttk.Radiobutton(reprocess_frame, text="Reverse Video",
                    variable=process_method,
                    value=4).grid(column=0, row=4, sticky=W)

    ok_btn = ttk.Button(reprocess_frame, text='Continue',
                        command=lambda:
                        process_image(username, process_method,
                                      reprocess_frame))
    ok_btn.grid(column=0, row=7)


if __name__ == '__main__':
    main()
