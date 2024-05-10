import tkinter as tk
import ttkbootstrap as ttk
from bs4 import BeautifulSoup as bs
from lxml import html
import requests
import sys
import classes as cs


if __name__ == '__main__':

    mainScreen = cs.Fullscreen_Window()
    #mainScreen.edit_text(5, 100)
    #mainScreen.edit_text(5, 100)
    mainScreen.toggle_button("przycisk")
    
    mainScreen.ttk.mainloop()


