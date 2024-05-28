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

busik = cs.transport()

busik.szwagropol('Kraków', 'Zakopane', '03:00', 'Sb')

print(busik.start)
print(busik.destination)
print(busik.top3_dep_time)
print(busik.top3_arr_time)
print(busik.day_label)


print('\nMajer przykład:')

busik2 = cs.transport()

busik2.majer('Kraków', 'Zakopane', '03:00', 'Sb')
print(busik2.start)
print(busik2.destination)
print(busik2.top3_dep_time)
print(busik2.top3_arr_time)
print(busik2.day_label)

pociag = cs.transport()

pociag.train('Nowy Sącz', 'Kraków Główny', '17:00', '28.05.2024')

print('\nPociag przykład:')
print(pociag.start)
print(pociag.destination)
print(pociag.train_name)
print(pociag.top3_dep_time)
print(pociag.top3_arr_time)
print(pociag.day_label)

pociag2 = cs.transport()
pociag2.train('Nowy Sącz', 'Piwniczna', '21:00', '28.05.2024')

print('\nPociag przykład:')
print(pociag2.start)
print(pociag2.destination)
print(pociag2.train_name)
print(pociag2.top3_dep_time)
print(pociag2.top3_arr_time)
print(pociag2.day_label)