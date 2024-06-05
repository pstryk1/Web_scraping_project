import tkinter as tk
import ttkbootstrap as ttk
from bs4 import BeautifulSoup as bs
from lxml import html
import requests
import sys
import classes as cs
import variables as var
from datetime import datetime




if __name__ == '__main__':
    #mainScreen = cs.FullscreenWindow()
    
    #mainScreen.ttk.mainloop()
    ble =  cs.busiordosalonik()
    timetable = sorted(ble.AD('Słomniki','Słomniki','15:00','2024-06-07'), key = lambda x: datetime.strptime(x[1],'%H:%M'))
    print(timetable)
    
    