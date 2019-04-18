from tkinter import *
from tkinter import ttk
# from tkinter.filedialog import askopenfilename
# from PIL import ImageTk, Image
from tkinter import filedialog
import requests
from pymodm import connect

root = Tk()  # makes main window
root.title("GUI Client")


def main():
    init_mongo_db()
    # first_screen()
    second_screen()


def init_mongo_db():
    connect("mongodb+srv://mlw60:Wm347609@bme547-r5nv9.mongodb.net/test?retryWrites=true")


def first_screen():
    top_label = ttk.Label(root, text="Please enter a username below:")
    top_label.grid(column=0, row=0)

    username = StringVar()
    username_entry = ttk.Entry(root, textvariable=username, width=25)
    username_entry.grid(column=0, row=1)

    browse_btn = ttk.Button(root, text='Upload Raw Image', command=browse_function)
    browse_btn.grid(column=0, row=2)

    ok_btn = ttk.Button(root, text='Continue', command=lambda: cont_function(username))
    ok_btn.grid(column=1, row=3)

    root.mainloop()  # shows window


def second_screen():
    top_label = ttk.Label(root, text="Select image processing steps:", font=("Helvetica", 20))
    top_label.grid(column=0, row=0)

    process_method = IntVar()
    im_display = IntVar()
    ttk.Radiobutton(root, text="Histogram Equalization", variable=process_method, value=1).grid(column=0, row=1, sticky=W)
    ttk.Radiobutton(root, text="Contrast Stretching", variable=process_method, value=2).grid(column=0, row=2, sticky=W)
    ttk.Radiobutton(root, text="Log Compression", variable=process_method, value=3).grid(column=0, row=3, sticky=W)
    ttk.Radiobutton(root, text="Reverse Video", variable=process_method, value=4).grid(column=0, row=4, sticky=W)

    Checkbutton(root, text='Display original and processed images',
                variable=im_display).grid(column=0, row=6, sticky=W, pady=20)
    ok_btn = ttk.Button(root, text='Continue',
                        command=lambda: process_image(process_method, im_display))
    ok_btn.grid(column=0, row=7)

    root.mainloop()  # shows window
    return im_display


def browse_function():
    global raw_filenames
    root.filename = filedialog.askopenfilenames(initialdir="/", title="Select file",
                                                filetypes=(("png files", "*.png"), ("all files", "*.*"),))
    raw_filenames = root.filename
    print(raw_filenames[0])


def cont_function(username):
    # send username to server
    new_user = {"user_name": username.get()
                }
    requests.post('http://127.0.0.1:5000/user_name', json=new_user)
    # goes to next page


def process_image(process_method, im_display):
    # figure out how to set hist eq as default
    if process_method.get() == 1:
        print('do hist eq')
    if process_method.get() == 2:
        print('do con stretch')
    if process_method.get() == 3:
        print('do log comp')
    if process_method.get() == 4:
        print('do reverse vid')

    if im_display.get() == 1:
        print('do image display')


if __name__ == '__main__':
    main()


