import tkinter as tk
import ttkbootstrap as ttk
from bs4 import BeautifulSoup as bs
from datetime import datetime
from lxml import html
import requests
import sys
import time

themes = ('darkly', 'flatly')


def polish_sign(word):
    signs = {
        'ą': '%C4%85',
        'ć': '%C4%87',
        'ę': '%C4%99',
        'ł': '%C5%82',
        'ń': '%C5%84',
        'ó': '%C3%83',
        'ś': '%C5%9B',
        'ź': '%C5%BA',
        'ż': '%C5%BC',
        'Ć': '%C4%86',
        'Ł': '%C5%81',
        'Ś': '%C5%9A',
        'Ź': '%C5%B9',
        'Ż': '%C5%BB'
    }
    for i in range(len(word)):
        if word[i] in signs:
            word = word.replace(word[i], signs[word[i]])
    return word


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
    elif bus == "Majer":
                all_labels = {
            '(1,7)': ('Pn','Wt','Śr','Czw','Pt','Sb','Nd'),
            '(5,6,7)': ('Pt','Sb','Nd'),
            '(6,7,1)': ('Sb','Nd','Pn'),
            '(6,7)': ('Sb','Nd'),
            '(5)': ('Pt'),
            '(6)': ('Sb'),
            '(7)': ('Nd'),
            '(1)': ('Pn'),
        }
    return all_labels[label]
    
class transport:

    def __init__(self):
        None

    def szwagropol(self, start, destination, planned_dep_time, day):

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
        self.top3_dep_time = tuple([i[0] for i in top3_results])
        self.top3_arr_time = tuple([i[1] for i in top3_results])
        self.day_label = day


    def majer(self, start, destination, planned_dep_time, day):
        page = 'https://www.majerbus.pl/pl/linia-regularna-zakopane-nowytarg-krakow'
        query = requests.get(page)
        scrape = bs(query.text, 'lxml')

        data_0 = [i.text.split() for i in scrape.find_all('table')]
        if start == 'Zakopane':
            data_0 = [i for i in data_0[0] if i.isalpha() == False]
        else:
            data_0 = [i for i in data_0[1] if i.isalpha() == False]

        data_1 = []
        for i in data_0:
            if len(i) > 7:
                i = i.split('(')
                data_1.append(i[0])
                data_1.append('('+i[1])
            elif len(i) == 4:
                data_1.append('0'+i)
            else:
                data_1.append(i)

        data_2 = []
        data_3 = []
        for i in data_1:
            if len(data_2) < 3:
                data_2.append(i)
            elif (i[0] == '(' or data_2[-1][0] == '(') and len(data_2) < 6:
                data_2.append(i)
            else:
                data_3.append(data_2)
                data_2 = []
                data_2.append(i)

        data_3.append(data_2)

        data_4 = []
        for i in data_3:
            if len(i) == 3:
                i.append(Labels('(1,7)', "Majer"))
                data_4.append([i[0],i[2],i[3]])
            else:
                i.append(Labels(i[1], "Majer"))
                data_4.append([i[0],i[4],i[6]])
            
        top3_results = []
        if start == 'Zakopane':
            for i in sorted(data_4, key= lambda o: abs(datetime.strptime(planned_dep_time, '%H:%M') - datetime.strptime(o[0], '%H:%M'))):
                if day in i[-1] and len(top3_results) < 3:
                    top3_results.append(i)
        else:
            for i in sorted(data_4, key= lambda o: abs(datetime.strptime(planned_dep_time, '%H:%M') - datetime.strptime(o[0], '%H:%M'))):
                if day in i[-1] and len(top3_results) < 3:
                    top3_results.append(i)
                    
        self.start = start
        self.destination = destination
        self.top3_dep_time = tuple([i[0] for i in top3_results])
        self.top3_arr_time = tuple([i[1] for i in top3_results])
        self.day_label = day


    def train(self, start, destination, planned_dep_time, date):


        
        start_check = start.split()

        if len(start_check) > 1:
            start_link = ''
            for i in start_check:
                start_link = start_link + '+' + i

        page = f'https://bilkom.pl/stacje/tablica?nazwa={start_link}&stacja=5100042&data={date.strip('.')}0000&time=00%3A00&przyjazd=false&_csrf='
        query = requests.get(page)
        scrape = bs(query.text, 'lxml')

        links = [i.a['href'] for i in scrape.find_all('div', class_='timeTableRow') if destination.split()[0] in [i.text.split()[5], i.text.split()[6], i.text.split()[7]]]

        scrape_links = []
        for i in links:
            page = f'https://bilkom.pl{i}'
            query = requests.get(page)
            scrape = bs(query.text, 'lxml')

            train_name = scrape.find('div', class_='carrier-metadata').text

            if len(start.split()) > 1 and len(destination.split()) > 1:
                data_0 = [i.text.split() for i in scrape.find_all('div', class_='trip') if (i.text.split()[-1] == start.split()[1] and i.text.split()[-2] == start.split()[0]) or (i.text.split()[-1] == destination.split()[1] and i.text.split()[-2] == destination.split()[0])]
            elif len(start.split()) > 1 and len(destination.split()) == 1:
                data_0 = [i.text.split() for i in scrape.find_all('div', class_='trip') if (i.text.split()[-1] == start.split()[1] and i.text.split()[-2] == start.split()[0]) or i.text.split()[-1] == destination.split()[0]]
            elif len(start.split()) == 1 and len(destination.split()) > 1:
                data_0 = [i.text.split() for i in scrape.find_all('div', class_='trip') if (i.text.split()[-1] == start.split()[0]) or (i.text.split()[-1] == destination.split()[1] and i.text.split()[-2] == destination.split()[0])]
            else:
                data_0 = [i.text.split() for i in scrape.find_all('div', class_='trip') if i.text.split()[-1] == start.split()[0] or i.text.split()[-1] == destination.split()[0]]

            if len(data_0[0]) > 10:
                print(data_0)
                scrape_links.append([train_name.strip(), data_0[0][6], data_0[1][1]])
            else:
                scrape_links.append([train_name.strip(), data_0[0][1], data_0[1][1]])

        top3_results = []
        for i in sorted(scrape_links, key= lambda o: abs(datetime.strptime(planned_dep_time, '%H:%M') - datetime.strptime(o[1], '%H:%M'))):
            if len(top3_results) < 3:
                top3_results.append(i)

        self.start = start
        self.destination = destination
        self.train_name = tuple([i[0] for i in top3_results])
        self.top3_dep_time = tuple([i[1] for i in top3_results])
        self.top3_arr_time = tuple([i[2] for i in top3_results])
        self.day_label = date
        


#print(train('27.05.2024', '3', ['Nowy', 'Sącz'], ['Kraków', 'Główny']))


def station_code(station):
    with open('train_stations.ini', 'r', encoding= 'utf8') as file:
        file = [[i.strip().split()[0]+i.strip().split()[1], i.strip().split()[2]] if len(i.strip().split()) > 2 else i.strip().split() for i in file.readlines()]
        print(file)

