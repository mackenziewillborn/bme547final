from tkinter import *
from tkinter import ttk
# from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
from tkinter import filedialog
import requests
from pymodm import connect

root = Tk()  # makes main window
root.title("GUI Client")
main_frame = Frame(root)
main_frame.pack()
raw_filepath = "/Users/kelseyli/Repos/bme547final/osa_lifecycle.png"
URL = "http://127.0.0.1:5000"


def main():
    init_mongo_db()
    username = first_screen()


def init_mongo_db():
    connect("mongodb+srv://mlw60:Wm347609@bme547-r5nv9."
            "mongodb.net/test?retryWrites=true")


def first_screen():
    first_frame = Frame(root)
    first_frame.pack()
    top_label = ttk.Label(first_frame, text="Please enter a username below:")
    top_label.grid(column=0, row=0)

    username = StringVar()
    username_entry = ttk.Entry(first_frame, textvariable=username, width=20)
    username_entry.grid(column=0, row=1)

    browse_btn = ttk.Button(first_frame, text='Upload Raw Image',
                            command=browse_function)
    browse_btn.grid(column=0, row=2)

    ok_btn = ttk.Button(first_frame, text='Continue',
                        command=lambda: cont_function(username, first_frame))
    ok_btn.grid(column=1, row=3)

    root.mainloop()  # shows window
    return username


def browse_function():
    global raw_filenames
    root.filename = \
        filedialog.askopenfilenames(initialdir="/", title="Select file",
                                    filetypes=(("png files", "*.png"),
                                               ("all files", "*.*"),))
    raw_filenames = root.filename
    print(raw_filenames[0])


def cont_function(username, first_frame):
    new_user = {"user_name": username.get()
                }
    requests.post(URL+'/user_name', json=new_user)


if __name__ == '__main__':
    main()
