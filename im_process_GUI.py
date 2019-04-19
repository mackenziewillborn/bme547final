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


def second_screen(username, first_frame):
    first_frame.destroy()
    second_frame = Frame(root)
    second_frame.pack()

    top_label = ttk.Label(second_frame,
                          text="Select image processing steps:",
                          font=("Helvetica", 20))
    top_label.grid(column=0, row=0)

    process_method = IntVar()
    im_display = IntVar()
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
    second_screen(username, first_frame)
    pass


def process_image(username, process_method, second_frame):
    # figure out how to set hist eq as default
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
                            "processing_type": processing_type}
    requests.post(URL+'/processing_type', json=user_processing_type)
    return


if __name__ == '__main__':
    main()
