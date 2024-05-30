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
            '(1-5)': ('poniedziałek','wtorek','środa','czwartek','piątek'),
            '(1-6)': ('poniedziałek','wtorek','środa','czwartek','piątek', 'sobota'),
            '(1-7)': ('poniedziałek','wtorek','środa','czwartek','piątek', 'sobota', 'niedziela'),
            '(5-7)': ('piątek', 'sobota', 'niedziela'),
            '(6-7)': ('sobota','niedziela'),
            '(1-5,7)': ('poniedziałek','wtorek','środa','czwartek','piątek', 'niedziela'),
            '(5)': ('piątek'),
            '(6)': ('sobota'),
            '(7)': ('niedziela')
        }
    elif bus == "Majer":
                all_labels = {
            '(1,7)': ('poniedziałek','wtorek','środa','czwartek','piątek', 'sobota', 'niedziela'),
            '(5,6,7)': ('piątek', 'sobota', 'niedziela'),
            '(6,7,1)': ('sobota','niedziela','poniedziałek'),
            '(6,7)': ('sobota', 'niedziela'),
            '(5)': ('piątek'),
            '(6)': ('sobota'),
            '(7)': ('niedziela'),
            '(1)': ('poniedziałek'),
        }
    return all_labels[label]

    
class transport:

    def __init__(self):
        self.is_connection = None
        self.start = None
        self.destination = None
        self.day_label = None
        self.train_name = []
        self.top5_dep_time = []
        self.top5_arr_time = []
        self.train_change_city = []


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

        top5_results = []
        if start == 'Nowy Sącz' or start == 'Zakopane':
            for i in sorted(data_2[1], key= lambda o: abs(datetime.strptime(planned_dep_time, '%H:%M') - datetime.strptime(o[0], '%H:%M'))):
                if day in Labels(i[2], 'Szwagropol') and len(top5_results) < 5:
                    top5_results.append(i)
        else:
            for i in sorted(data_2[0], key= lambda o: abs(datetime.strptime(planned_dep_time, '%H:%M') - datetime.strptime(o[0], '%H:%M'))):
                if day in Labels(i[2], 'Szwagropol') and len(top5_results) < 5:
                    top5_results.append(i)            

        self.start = start
        self.destination = destination
        self.top5_dep_time = tuple([i[0] for i in top5_results])
        self.top5_arr_time = tuple([i[1] for i in top5_results])
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
            
        top5_results = []
        if start == 'Zakopane':
            for i in sorted(data_4, key= lambda o: abs(datetime.strptime(planned_dep_time, '%H:%M') - datetime.strptime(o[0], '%H:%M'))):
                if day in i[-1] and len(top5_results) < 5:
                    top5_results.append(i)
        else:
            for i in sorted(data_4, key= lambda o: abs(datetime.strptime(planned_dep_time, '%H:%M') - datetime.strptime(o[0], '%H:%M'))):
                if day in i[-1] and len(top5_results) < 5:
                    top5_results.append(i)
                    
        self.start = start
        self.destination = destination
        self.top5_dep_time = tuple([i[0] for i in top5_results])
        self.top5_arr_time = tuple([i[1] for i in top5_results])
        self.day_label = day

        
    def train(self, start, destination, planned_dep_time, date):

        def station_code(station):
            with open('Hafas_Codes.csv', 'r', encoding= 'utf8') as file:
                data = {
                    i.split(';')[0]:i.split(';')[1].strip() for i in file.readlines()
                }
                return data[station]
            
        def station_name_code(station):
            if len(station) > 1:
                station_link = ''
                for i in station:
                    if station_link != '':
                        station_link = station_link + '+' + i
                    else:
                        station_link = i
                return station_link
            return station[0]
        
        start_link = station_name_code(start.split())
        destination_link = station_name_code(destination.split())

        
        if planned_dep_time[:2] != '00' and int(planned_dep_time[:2]) > 10:
            page = f'https://bilkom.pl/podroz?basketKey=&carrierKeys=PZ%2CP2%2CP1%2CP5%2CP7%2CP4%2CP9%2CP0%2CO1%2CP3%2CP6%2CP8&trainGroupKeys=G.EXPRESS_TRAINS%2CG.FAST_TRAINS%2CG.REGIONAL_TRAINS&fromStation={start_link}&poczatkowa=A%3D1%40O%3D{start_link}%40X%3D19947423%40Y%3D50067192%40U%3D51%40L%3D{station_code(start_link)}%40B%3D1%40p%3D1716898916%40&toStation={destination_link}&docelowa=A%3D1%40O%3D{destination_link}%40X%3D22006798%40Y%3D50043110%40U%3D51%40L%3D{station_code(destination_link)}%40B%3D1%40p%3D1716898916%40&middleStation1=&posrednia1=&posrednia1czas=&middleStation2=&posrednia2=&posrednia2czas=&data={date.replace('.','')}{str(int(planned_dep_time[:2])-1)+planned_dep_time[-2:]}&date={date[:2]}%2F{date[3:5]}%2F{date[-4:]}&time={str(int(planned_dep_time[:2])-1)}%3A{planned_dep_time[-2:]}&minChangeTime=10&przyjazd=false&_csrf='
        elif int(planned_dep_time[:2]) <= 10:
            page = f'https://bilkom.pl/podroz?basketKey=&carrierKeys=PZ%2CP2%2CP1%2CP5%2CP7%2CP4%2CP9%2CP0%2CO1%2CP3%2CP6%2CP8&trainGroupKeys=G.EXPRESS_TRAINS%2CG.FAST_TRAINS%2CG.REGIONAL_TRAINS&fromStation={start_link}&poczatkowa=A%3D1%40O%3D{start_link}%40X%3D19947423%40Y%3D50067192%40U%3D51%40L%3D{station_code(start_link)}%40B%3D1%40p%3D1716898916%40&toStation={destination_link}&docelowa=A%3D1%40O%3D{destination_link}%40X%3D22006798%40Y%3D50043110%40U%3D51%40L%3D{station_code(destination_link)}%40B%3D1%40p%3D1716898916%40&middleStation1=&posrednia1=&posrednia1czas=&middleStation2=&posrednia2=&posrednia2czas=&data={date.replace('.','')}{'0'+str(int(planned_dep_time[:2])-1)+planned_dep_time[-2:]}&date={date[:2]}%2F{date[3:5]}%2F{date[-4:]}&time={str(int(planned_dep_time[:2])-1)}%3A{planned_dep_time[-2:]}&minChangeTime=10&przyjazd=false&_csrf='  
        else:
            page = f'https://bilkom.pl/podroz?basketKey=&carrierKeys=PZ%2CP2%2CP1%2CP5%2CP7%2CP4%2CP9%2CP0%2CO1%2CP3%2CP6%2CP8&trainGroupKeys=G.EXPRESS_TRAINS%2CG.FAST_TRAINS%2CG.REGIONAL_TRAINS&fromStation={start_link}&poczatkowa=A%3D1%40O%3D{start_link}%40X%3D19947423%40Y%3D50067192%40U%3D51%40L%3D{station_code(start_link)}%40B%3D1%40p%3D1716898916%40&toStation={destination_link}&docelowa=A%3D1%40O%3D{destination_link}%40X%3D22006798%40Y%3D50043110%40U%3D51%40L%3D{station_code(destination_link)}%40B%3D1%40p%3D1716898916%40&middleStation1=&posrednia1=&posrednia1czas=&middleStation2=&posrednia2=&posrednia2czas=&data={date.replace('.','')}{planned_dep_time.replace(':','')}&date={date[:2]}%2F{date[3:5]}%2F{date[-4:]}&time={planned_dep_time.replace(':','')}%3A{planned_dep_time[-2:]}&minChangeTime=10&przyjazd=false&_csrf='
        print(page)
        query = requests.get(page)
        scrape = bs(query.text, 'lxml')

        tables = [i.find_all('tr') for i in scrape.find_all('table', class_='table table-hover table-carriers')]
        results = []
        for table in tables:
            all_rows = []
            for row in table:
                all_rows.append(row.text.split())

            result_rows = []
            for i in range(len(all_rows)):
                all_rows_new = []
                word = ''
                if i % 2 == 0:
                    for k in all_rows[i]:
                        if k == '-':
                            break
                        elif k.isalpha() == True:
                            if word != '':
                                word = word + ' ' + k
                            else:
                                word = k
                        elif k != '|':
                            all_rows_new.append(k)
                    if word != '':
                        all_rows_new.append(word)
                else:
                    all_rows_new = all_rows[i][0]+' '+all_rows[i][1]
                result_rows.append(all_rows_new)
            results.append(result_rows)
    
        if len(results) == 0:
            self.is_connection = False
            self.start = start
            self.destination = destination
            self.day_label = date
        else: 
            self.is_connection = True
            self.start = start
            self.destination = destination
            self.day_label = date
            self.train_name = []
            self.top6_dep_time = []
            self.top6_arr_time = []
            self.train_change_city = []

            for i in results:

                if len(self.top6_dep_time) == 6:
                    break

                if len(i) == 3:
                    self.train_name.append(i[1])
                    self.top6_dep_time.append(i[0][0])
                    self.top6_arr_time.append(i[2][0])
                else:
                    self.train_name.append([i[k] for k in range(len(i)) if k % 2 == 1])
                    self.top6_dep_time.append(i[0][0])
                    self.top6_arr_time.append(i[-1][0])
                    
                    self.train_change_city.append([[i[k][-2], i[k][-1]] for k in range(len(i)) if k % 2 == 0 and i[k] is not i[0] and i[k] is not i[-1]])



