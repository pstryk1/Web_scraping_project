import tkinter as tk
import ttkbootstrap as ttk
from bs4 import BeautifulSoup as bs
from lxml import html
import requests
import sys
from datetime import datetime
import classes as cs
import variables as var
from PIL import Image
Image.CUBIC = Image.BICUBIC

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

    





#print(search_transport('Nowy Sącz', 'Kraków Główny', '12:00', '30.06.2024'))
#print(search_transport('Zakopane', 'Kraków Główny', '12:00', '05.06.2024'))
#print(search_transport('Kraków Główny', 'Słomniki', '11:00', '11.06.2024'))

'''
ab = cs.transport()

ab.train('Kraków Główny', 'Niedźwiedź', '10:00', '2024-06-11')

print(ab.start)
print(ab.destination)
print(ab.top6_dep_time)
print(ab.top6_arr_time)

'''
