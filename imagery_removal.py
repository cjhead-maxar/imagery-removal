import os
import tkMessageBox
from getpass import getuser
from Tkinter import *
from ttk import *

# Suffixes of imagery targeted for removal
# Be as specific as possible
SUFFIXES = (
    "ard_mosaic_ms.tif",
    "ard_mosaic_ms.aux",
    "ard_mosaic_ms_combo.tif",
    "ard_mosaic_ms_combo.aux",
    "ard_maxardem.tif",
    "ard_maxardem.aux",
    "imagery_nostat.img",
    "imagery_nostat.ige",
    "imagery.img",
    "climate.tif",
    "dem.img",
    "vn.img",
    ".aux",
    "imagery.ige"
)

def recursive_image_Search(start_path, images, suffixes=SUFFIXES):

    for path in os.listdir(start_path):
        path = os.path.join(start_path, path)

        if os.path.isfile(path):
            if path.endswith(suffixes):
                images.append(path)

        elif os.path.isdir(path):
            images = recursive_image_Search(path, images)

    return images


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(sticky=NSEW)
        self.createWidgets()

        style = Style()
        style.theme_use('alt')

        style.configure('TLabel',
            background='light blue')

        style.configure('TLabelframe',
            padding=15,
            background='light blue')

        style.configure('TFrame',
            background='light blue')

        style.configure('TButton',
            background='light blue')

    def find_imagery(self):

        user = getuser()
        stargazer = r"C:\Users\{}\Desktop\GeoCue_Data".format(user)
        blaze = r"D:\GeoCue_Data"

        if os.path.exists(stargazer):
            return self.delete_imagery(stargazer)

        elif os.path.exists(blaze):
            return self.delete_imagery(blaze)

    def delete_imagery(self, system):

        image_list = []
        images = recursive_image_Search(system, image_list)
        images_text = "\n".join(images)

        window2 = Toplevel()
        window2.resizable(width=True, height=True)
        window2.rowconfigure(0, weight=1)
        window2.columnconfigure(0, weight=1)

        frame1 = Frame(window2)
        frame1.grid(sticky=NSEW)
        frame1.rowconfigure(0, weight=1)
        frame1.rowconfigure(1, weight=1)
        frame1.rowconfigure(2, weight=1)
        frame1.columnconfigure(0, weight=1)
        frame1.columnconfigure(1, weight=1)

        textlabel1 = Label(frame1, text="Imagery")

        labelframe1 = LabelFrame(frame1, labelwidget=textlabel1)
        labelframe1.grid(row=0, column=0, columnspan=2, sticky=NSEW)
        labelframe1.rowconfigure(0, weight=1)
        labelframe1.columnconfigure(0, weight=1)

        scrollbar1 = Scrollbar(labelframe1)
        scrollbar1.grid(row=0, column=1, sticky=NSEW)

        textbox1 = Text(labelframe1)
        textbox1.grid(row=0, column=0, sticky=NSEW)
        textbox1.insert('insert', images_text)
        textbox1['bg'] = 'light blue'
        textbox1['yscrollcommand'] = scrollbar1.set
        textbox1['state'] = DISABLED

        scrollbar1['command'] = textbox1.yview

        label1 = Label(frame1, text="Delete All Imagery?", anchor=CENTER)
        label1.grid(row=1, column=0, columnspan=2, sticky=NSEW)

        button1 = Button(frame1, text="Yes", command=lambda:self.confirm_delete(window2, images))
        button1.grid(row=2, column=0, sticky=NSEW)

        button2 = Button(frame1, text="No", command=window2.destroy)
        button2.grid(row=2, column=1, sticky=NSEW)

    def confirm_delete(self, window, images):

        window.destroy()

        remove = os.remove
        for image in images:
            remove(image)

        tkMessageBox.showinfo("Imagery Deleted", "Imagery Has Been Deleted!")

    def createWidgets(self):

        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1, minsize=100)
        top.columnconfigure(0, weight=1, minsize=300)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.button1 = Button(self, text="Find Imagery", command=self.find_imagery)
        self.button1.grid(row=0, column=0, sticky=NSEW)


app = Application()
app.master.title("Imagery Removal")
app.mainloop()