import requests
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import requests

root = Tk()
root.title("GUI Client")

URL = "http://127.0.0.1:5000"


def new_window1(username):
    newwin1 = Toplevel(root)
    second_screen(username, newwin1)


def first_screen():
    top_label = ttk.Label(root, text="Please enter a username below:")
    top_label.grid(column=0, row=0)

    username = StringVar()
    username_entry = ttk.Entry(root, textvariable=username, width=25)
    username_entry.grid(column=0, row=1)

    ok_btn = ttk.Button(root, text='Enter', command=lambda: cont_function(username))
    ok_btn.grid(column=1, row=1)

    # browse_btn = ttk.Button(root, text='Upload Raw Image', command=browse_function)
    # browse_btn.grid(column=0, row=2)

    cont_btn = ttk.Button(root, text='Continue', command=lambda: new_window1(username))
    cont_btn.grid(column=1, row=3)

    return username


def cont_function(username):
    user_user = {"user_name": username.get()}
    requests.post(URL+'/user_name', json=user_user)


# def browse_function():
#     global raw_filenames
#     root.filename = filedialog.askopenfilenames(initialdir="/", title="Select file",
#                                                 filetypes=(("png files", "*.png"), ("all files", "*.*"),))
#     raw_filenames = root.filename
#     print(raw_filenames[0])


def second_screen(username, newwin1):
    top_label = ttk.Label(newwin1, text="Select image processing steps:", font=("Helvetica", 20))
    top_label.grid(column=0, row=0)

    process_method = IntVar()
    im_display = IntVar()
    ttk.Radiobutton(newwin1, text="Histogram Equalization", variable=process_method, value=1).grid(column=0, row=1,
                                                                                                sticky=W)
    ttk.Radiobutton(newwin1, text="Contrast Stretching", variable=process_method, value=2).grid(column=0, row=2, sticky=W)
    ttk.Radiobutton(newwin1, text="Log Compression", variable=process_method, value=3).grid(column=0, row=3, sticky=W)
    ttk.Radiobutton(newwin1, text="Reverse Video", variable=process_method, value=4).grid(column=0, row=4, sticky=W)

    Checkbutton(newwin1, text='Display original and processed images',
                variable=im_display).grid(column=0, row=6, sticky=W, pady=20)
    ok_btn = ttk.Button(newwin1, text='Continue',
                        command=lambda: process_image(process_method, im_display, username))
    ok_btn.grid(column=0, row=7)


def process_image(process_method, im_display, username):
    processing_type = []
    if process_method.get() == 1:
        processing_type = 'do hist eq'
    if process_method.get() == 2:
        processing_type = 'do con stretch'
    if process_method.get() == 3:
        processing_type = 'do log comp'
    if process_method.get() == 4:
        processing_type = 'do reverse vid'

    if im_display.get() == 1:
        imagedisplay = 'do image display'
    else:
        imagedisplay = 'dont do image display'

    user_processing_type = {"user_name": username.get(),
                            "processing_type": processing_type,
                            "image_display": imagedisplay}
    requests.post(URL+'/processing_type', json=user_processing_type)


if __name__ == "__main__":
    username = first_screen()
    root.mainloop()

