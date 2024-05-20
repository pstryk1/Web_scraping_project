import tkinter as tk
import ttkbootstrap as ttk
from bs4 import BeautifulSoup as bs
from lxml import html
import requests
import sys
import classes as cs
import variables as var

def start():
    #startScreen.destroy()
    mainScreen = cs.FullscreenWindow()
    mainScreen.ttk.mainloop()


if __name__ == '__main__':
    start()
    """
    startScreen = ttk.Window()
    startScreen.title("QuoCalCus - zkalkuluj swoją drogę!")
    startScreen.iconbitmap("images/logo_darkblue_copy.ico")
    startScreen.state('zoomed')

    slabel = ttk.Label(startScreen, text="Start")
    slabel.pack()
    startScreen.after(1000, start)
    startScreen.mainloop()
    
    """

    