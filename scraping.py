import tkinter as tk
import ttkbootstrap as ttk
from bs4 import BeautifulSoup as bs
from lxml import html
import requests
import sys
import classes as cs
import variables as var




if __name__ == '__main__':
    #mainScreen = cs.FullscreenWindow()
    
    #mainScreen.ttk.mainloop()
    ble =  cs.busiordosalonik('Słomniki','Słomniki','19:00','28')
    timetable = ble.AD()
    print(timetable)
    
    