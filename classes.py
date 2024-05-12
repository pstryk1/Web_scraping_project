import tkinter as tk
import ttkbootstrap as ttk
from bs4 import BeautifulSoup as bs
from datetime import datetime
from lxml import html
import requests
import sys

themes = ('darkly', 'flatly')

def Labels(label, bus):
    if bus == "Szwagropol":
        all_labels = {
            '(1-5)': 'Pn-Pt',
            '(1-6)': 'Pn-Sb',
            '(5-7)': 'Pt-Nd',
            '(6-7)': 'Sb-Nd',
            '(1-5,7)': 'Nd-Pt',
            '(5)': 'Pt',
            '(6)': 'Sb',
            '(7)': 'Nd'
        }

    return all_labels[label]

def Maxbus_scrapped():
    page1 = 'https://maxbus.com.pl/rozklad/krakow-zegocina-laskowa-limanowa/'
    query = requests.get(page1)
    scrape = bs(query.text, 'html.parser')
    #body = scrap.body
    tab = scrape.find('tbody')
    #col = tab.find_all('col')
    return tab

def Szwagropol(start, destination):
    if start  == 'NS' or destination == 'NS':
        page = 'https://www.szwagropol.pl/pl/linie-autobusowe/rozklad-jazdy/?rozklad=2&kierunek=6'
    elif start  == 'ZAK' or destination == 'ZAK':
        page = 'https://www.szwagropol.pl/pl/linie-autobusowe/rozklad-jazdy/?rozklad=1&kierunek=2'

    query = requests.get(page)
    scrape = bs(query.text, 'html.parser')
    data_1 = [i.text.split() for i in scrape.find_all('table')]

    unwanted = ['Odjazd','Przyjazd','Szczegóły', 'trasy']
    data_2 = []

    for i in data_1:
        data_3 = []
        data_4 = []
        label = 'Pn-Nd'

        for j in i:
            if j not in unwanted:
                if len(data_4) != 2:
                    data_4.append(j[:5])
                    if len(j) > 5:
                        label = Labels(j[5:], 'Szwagropol')
                else:
                    data_4.append(label)
                    data_3.append(tuple(data_4))
                    label = 'Pn-Nd'
                    data_4 = []
                    data_4.append(j[:5])

        data_4.append(label)
        data_3.append(tuple(data_4))
        data_2.append(tuple(data_3))

    return tuple(data_2)

class Fullscreen_Window:

    def __init__(self):
        self.ttk = ttk.Window(themename=themes[0])
        self.ttk.attributes("-topmost", True)
        
        #self.tk.geometry("{0}x{1}+0+0".format(self.tk.winfo_screenwidth(), self.tk.winfo_screenheight()))
        self.ttk.state('zoomed')
        self.frame = ttk.Frame(self.ttk)
        self.frame.pack()
        self.state = False
        self.ttk.bind("<F11>", self.toggle_fullscreen)
        self.ttk.bind("<Escape>", self.end_fullscreen)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.ttk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.ttk.attributes("-fullscreen", False)
        return "break"
    
    def colors(self, color, fontcolor):
        self.ttk.configure(bg=color, fg = fontcolor)

    def edit_text(self,  height, width):
        edit_text = tk.Text(height=height, width=width, font=("Arial", 12), bd=2, relief="groove", padx=10, pady=10)
        edit_text.pack() #expand=False, fill="both"
        return edit_text.get("1.0", "end-1c")
    
    def toggle_button(self, text):

        def bfun(self, var):
            self.style = themes[int(var)]

        var1 = 0 #tk.IntVar()
        toggle = ttk.Checkbutton(
            bootstyle = "dange, round-toggle",
            text = text,
            variable=var1, 
            onvalue = 0, 
            offvalue=1,
            command=bfun(self, var1))
        toggle.pack(pady = 10)



class bus:

    def __init__(self):
        self.start = None
        self.destination = None
        self.top3_dep_time = None
        self.top3_arr_time = None
        self.day_label = None

    def szwagropol(self, start, destination, planned_dep_time, day):

        def Labels(label, bus):
            if bus == "Szwagropol":
                all_labels = {
                    '(1-5)': ('Pn','Wt','Śr','Czw','Pt'),
                    '(1-6)': ('Pn','Wt','Śr','Czw','Pt','Sb'),
                    '(1-7)': ('Pn','Wt','Śr','Czw','Pt','Sb','Nd'),
                    '(5-7)': ('Pt','Sb','Nd'),
                    '(6-7)': ('Sb','Nd'),
                    '(1-5,7)': ('Pn','Wt','Śr','Czw','Pt','Nd'),
                    '(5)': ('Pt'),
                    '(6)': ('Sb'),
                    '(7)': ('Nd')
                }

            return all_labels[label]

        if start  == 'Nowy Sącz' or destination == 'Nowy Sącz':
            page = 'https://www.szwagropol.pl/pl/linie-autobusowe/rozklad-jazdy/?rozklad=2&kierunek=6'
        elif start  == 'Zakopane' or destination == 'Zakopane':
            page = 'https://www.szwagropol.pl/pl/linie-autobusowe/rozklad-jazdy/?rozklad=1&kierunek=2'

        query = requests.get(page)
        scrape = bs(query.text, 'html.parser')
        data_1 = [i.text.split() for i in scrape.find_all('table')]

        unwanted = ['Odjazd','Przyjazd','Szczegóły', 'trasy']
        data_2 = []

        for i in data_1:
            data_3 = []
            data_4 = []
            label = '(1-7)'

            for j in i:
                if j not in unwanted:
                    if len(data_4) != 2:
                        data_4.append(j[:5])
                        if len(j) > 5:
                            label = j[5:]
                    else:
                        data_4.append(label)
                        data_3.append(tuple(data_4))
                        label = '(1-7)'
                        data_4 = []
                        data_4.append(j[:5])

            data_4.append(label)
            data_3.append(tuple(data_4))
            data_2.append(tuple(data_3))

        top3_results = []
        if start == 'Nowy Sącz' or start == 'Zakopane':
            for i in sorted(data_2[1], key= lambda o: abs(datetime.strptime(planned_dep_time, '%H:%M') - datetime.strptime(o[0], '%H:%M'))):
                if day in Labels(i[2], 'Szwagropol') and len(top3_results) < 3:
                    top3_results.append(i)
        else:
            for i in sorted(data_2[0], key= lambda o: abs(datetime.strptime(planned_dep_time, '%H:%M') - datetime.strptime(o[0], '%H:%M'))):
                if day in Labels(i[2], 'Szwagropol') and len(top3_results) < 3:
                    top3_results.append(i)            

        self.start = start
        self.destination = destination
        self.top3_arr_time = tuple([i[0] for i in top3_results])
        self.top3_dep_time = tuple([i[1] for i in top3_results])
        self.day_label = day









    #def find_connection(self, time, day):







#print(Szwagropol('ZAK'))