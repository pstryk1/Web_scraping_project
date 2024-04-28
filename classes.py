import tkinter as tk
import ttkbootstrap as ttk
from bs4 import BeautifulSoup as bs
from lxml import html
import requests
import sys

class Fullscreen_Window:

    def __init__(self):
        self.tk = tk.Tk()
        self.tk.attributes("-topmost", True)
        #self.tk.geometry("{0}x{1}+0+0".format(self.tk.winfo_screenwidth(), self.tk.winfo_screenheight()))
        self.tk.state('zoomed')
        self.frame = tk.Frame(self.tk)
        self.frame.pack()
        self.state = False
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"
    
    def colors(self, color, fontcolor):
        self.tk.configure(bg=color, fg = fontcolor)

    def edit_text(self,  height, width):
        edit_text = tk.Text(height=height, width=width, font=("Arial", 12), bd=2, relief="groove")
        edit_text.pack() #expand=False, fill="both"
        return edit_text.get("1.0", "end-1c")


