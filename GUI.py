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
    first_screen()


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


if __name__ == '__main__':
    main()


