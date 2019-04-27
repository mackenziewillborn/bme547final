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


def third_screen(username, second_frame):
    second_frame.destroy()
    third_frame = Frame(root)
    third_frame.pack()

    # r = requests.get(URL+'/time_uploaded/'+username.get())
    # r_json = r.json()
    # print(r_json)
    # time_uploaded = r_json['time_uploaded']
    # print(time_uploaded)
    # ttk.Label(third_frame, text="Time Uploaded: {}".
    #           format(time_uploaded)).grid(column=0,
    #                                       row=0, columnspan=2, sticky=W)

    # r = requests.get(URL+"/process_time/username")
    # process_time = r.text
    # ttk.Label(root, text="Time to Process: {}".
    #           format(process_time)).grid(column=0,
    #                                      row=1, columnspan=2, sticky=W)
    ttk.Label(third_frame,
              text="Time to Process: ").grid(column=0, row=1,
                                             sticky=W)

    # r = requests.get(URL+"/image_size/username")
    # image_size = r.text
    # ttk.Label(root, text="Image Size: {}".
    #           format(image_size)).grid(column=0,
    #           row=2, columnspan=2, sticky=W)
    ttk.Label(third_frame,
              text="Image Size:").grid(column=0, row=2,
                                       sticky=W)

    ok_btn = ttk.Button(third_frame,
                        text='Raw vs. Processed Images',
                        command=lambda: image_window())
    ok_btn.grid(column=0, row=3)

    image_download = ttk.Label(third_frame,
                               text="Download processed image as:")
    image_download.grid(column=3, row=0,
                        rowspan=2, columnspan=2, sticky=W)

    image_format = StringVar()
    ttk.Radiobutton(third_frame, text='JPEG',
                    variable=image_format,
                    value='JPEG').grid(column=3, row=2, sticky=W)
    ttk.Radiobutton(third_frame,
                    text='PNG', variable=image_format,
                    value='PNG').grid(column=3, row=3, sticky=W)
    ttk.Radiobutton(third_frame,
                    text='TIFF', variable=image_format,
                    value='TIFF').grid(column=3, row=4, sticky=W)

    ok_btn = ttk.Button(third_frame, text='Download',
                        command=download_function)
    ok_btn.grid(column=4, row=6)
    reprocess_btn = ttk.Button(third_frame,
                               text='Apply another Processing Method',
                               command=lambda:
                               reprocess_function(username, third_frame))
    reprocess_btn.grid(column=3, row=6)

    root.mainloop()  # shows window
    return third_frame


def browse_function():
    global raw_filenames
    root.filename = \
        filedialog.askopenfilenames(initialdir="/", title="Select file",
                                    filetypes=(("png files", "*.png"),
                                               ("all files", "*.*"),))
    raw_filenames = root.filename


def cont_function(username, first_frame):
    new_user = {"user_name": username.get()
                }
    # requests.post(URL+'/user_name', json=new_user)
    second_screen(username, first_frame)
    pass


def process_image(username, process_method, second_frame):
    # with open(raw_filenames[0], "rb") as raw_image_file:
    #     raw_b64_bytes = base64.b64encode(raw_image_file.read())
    # raw_b64_string = str(raw_b64_bytes, encoding='utf-8')
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

    # user_processing_type = {"user_name": username.get(),
    #                         "raw_b64_string": raw_b64_string,
    #                         "processing_type": processing_type}
    # requests.post(URL+'/processing_type', json=user_processing_type)

    third_screen(username, second_frame)
    return


def image_window():
    image_win = Toplevel(root)

    raw_open = Image.open(raw_filepath)
    raw_image = ImageTk.PhotoImage(raw_open)

    proc_open = Image.open("osa_lifecycle.png")
    # change eventually to processed image
    proc_image = ImageTk.PhotoImage(proc_open)

    panel1 = Label(image_win, image=raw_image)
    panel1.grid(row=0, column=0)
    panel1 = Label(image_win, text="Raw Image")
    panel1.grid(row=1, column=0)

    panel2 = Label(image_win, image=proc_image)
    panel2.grid(row=0, column=1)
    panel1 = Label(image_win, text="Processed Image")
    panel1.grid(row=1, column=1)
    root.mainloop()


def download_function():
    print('download')


def reprocess_function(username, third_frame):
    # can change this
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
