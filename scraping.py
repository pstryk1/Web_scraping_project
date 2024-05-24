import tkinter as tk
import ttkbootstrap as ttk
from bs4 import BeautifulSoup as bs
from lxml import html
import requests
import sys
import classes as cs


#if __name__ == '__main__':

    #mainScreen = cs.Fullscreen_Window()
    #mainScreen.edit_text(5, 100)
    #mainScreen.edit_text(5, 100)
    #mainScreen.toggle_button("przycisk")
    
    #mainScreen.ttk.mainloop()

print('Szwagropol przykład:')

busik = cs.bus()

busik.szwagropol('Kraków', 'Zakopane', '03:00', 'Sb')

print(busik.start)
print(busik.destination)
print(busik.top3_dep_time)
print(busik.top3_arr_time)
print(busik.day_label)


print('\nMajer przykład:')

busik2 = cs.bus()

busik2.majer('Kraków', '03:00', 'Sb')
print(busik2.start)
print(busik2.destination)
print(busik2.top3_dep_time)
print(busik2.top3_arr_time)
print(busik2.day_label)