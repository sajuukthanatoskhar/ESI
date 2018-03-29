#Moon Goo Gui

from tkinter import *
import tkinter


class Window(Frame):
    def __init__(self, master= None):
        Frame.__init__(self,master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("GUI")
        self.pack(fill=BOTH, expand=1)
        quitButton = Button(self, text="Quit",command=self.client_exit)
        quitButton.place(x=0,y=0)
        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label="Exit", command=self.client_exit)

        # added "file" to our menu
        menu.add_cascade(label="File", menu=file)

        # create the file object)
        edit = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        edit.add_command(label="Undo")

        # added "file" to our menu
        menu.add_cascade(label="Edit", menu=edit)

    def client_exit(self):
        exit()


def callback(msg):
    print(msg)

def MoonGooGui():

    root = Tk()
    root.geometry("400x300")
    app = Window(root)
    root.mainloop()

