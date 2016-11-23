from tkinter import *
from tkinter import ttk


class MainFrame(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_gui()

    def parse(self):

    def init_gui(self):
        """Builds GUI."""
        self.root.title('My Little Parser')

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

if __name__ == '__main__':
    root = Tk()
    MainFrame(root)
    root.mainloop()
