import requests
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import requests

root = Tk()
root.title("GUI Client")

URL = "http://127.0.0.1:5000"


def first_screen():
    top_label = ttk.Label(root, text="Please enter a username below:")
    top_label.grid(column=0, row=0)

    username = StringVar()
    username_entry = ttk.Entry(root, textvariable=username, width=25)
    username_entry.grid(column=0, row=1)

    ok_btn = ttk.Button(root, text='Continue', command=lambda: cont_function(username))
    ok_btn.grid(column=1, row=3)

    root.mainloop()
    return username


def cont_function(username):
    user_user = {"user_name": username.get()}
    r = requests.post(URL+'/user_name', json=user_user)


if __name__ == "__main__":
    username = first_screen()
    cont_function(username)
