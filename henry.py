import tkinter as tk
from tkinter import ttk
from henrySBA import HenrySBA
from henrySBC import HenrySBC
from henrySBP import HenrySBP

class HenryApp:
    def __init__(self, root):
        self.notebook = ttk.Notebook(root)

        frame_sba = ttk.Frame(self.notebook)
        frame_sbc = ttk.Frame(self.notebook)
        frame_sbp = ttk.Frame(self.notebook)

        self.notebook.add(frame_sba, text="Search by Author")
        self.notebook.add(frame_sbc, text="Search by Category")
        self.notebook.add(frame_sbp, text="Search by Publisher")
        self.notebook.pack(expand=1, fill="both")

        HenrySBA(frame_sba)
        HenrySBC(frame_sbc)
        HenrySBP(frame_sbp)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Henry Bookstore") 
    app = HenryApp(root)
    root.mainloop()
