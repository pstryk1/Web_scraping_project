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


busik = cs.bus()

busik.szwagropol('Kraków','Nowy Sącz', '08:00', 'Sb')

print(busik.start)
print(busik.destination)
print(busik.top3_arr_time[0])
print(busik.top3_dep_time[0])
print(busik.day_label)