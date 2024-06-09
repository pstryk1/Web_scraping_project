import tkinter as tk
import ttkbootstrap as ttk
from bs4 import BeautifulSoup as bs
from datetime import datetime
from lxml import html
import requests
import sys
from datetime import date
import variables as var
import webbrowser as web
import csv
import searching as search

themes = ('quocalcus', 'flatly')
import time



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






class FullscreenWindow:

    def __init__(self):
        super().__init__()
        
        self.ttk = ttk.Window(themename=themes[0])
        self.ttk.title("QuoCalCus - zkalkuluj swoją drogę!")
        self.ttk.iconbitmap("images/logo_darkblue_copy.ico")
        #self.ttk.attributes("-topmost", True)
        #self.tk.geometry("{0}x{1}+0+0".format(self.tk.winfo_screenwidth(), self.tk.winfo_screenheight()))
        self.ttk.grid_columnconfigure(0, weight=1)
        self.ttk.grid_rowconfigure(1, weight=0)

        self.ttk.state('zoomed')
        self.current_theme= 0
        self.toggle_button()
        

        SearchSettings(self) #tworzenie obiektu do wyszukiwania
        self.ramka= tk.Frame( bd=2, relief="solid", padx=10, pady=10, width=100)
        self.ramka.config()
        self.ramka.grid(padx = 10, pady = 10, row = 2, column=0, sticky='n')
        #self.frame['borderwidth'] = 1
        self.label1 = ttk.Label(text='Wyniki wyszukiwania', font=("Monsterrat", 15))
        self.label1.grid(padx = 10, pady = 10, row = 2, column=0, sticky='n')
        self.label1.grid_rowconfigure(2, weight=2)
        #
        
        

        self.state = False
        self.ttk.bind("<F11>", self.toggle_fullscreen)
        self.ttk.bind("<Escape>", self.end_fullscreen)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  
        self.ttk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.ttk.attributes("-fullscreen", False)
        return "break"
    #####################################################

    def label_update(self, sv):
        self.napis.config(text=sv.get())


    def colors(self, color, fontcolor):
        self.ttk.configure(bg=color, fg = fontcolor)

    def edit_text(self,  height, width, r, c, px, py):
        edit_text = tk.Text(height=height, width=width, font=("Arial", 12), bd=2, relief="solid", padx=10, pady=10)
        edit_text.grid(r, c)
        return edit_text.get("1.0", "end-1c")  

    def toggle_button(self):
        def bfun():
            self.ttk.style.theme_use(themes[var1.get()])
            self.toggle.configure(text=themes[var1.get()].capitalize())


        var1 = ttk.IntVar()
        self.toggle = ttk.Checkbutton(
            bootstyle = "danger, round-toggle",
            text = "Dark",
            variable=var1, 
            onvalue = 1, 
            offvalue=0,
            command=bfun)
        self.toggle.grid(padx = 10, pady = 10, row = 0, column=0, sticky='e')

#---------------------------------------------------------------------------------------------------------------------------#        

class SearchSettings(ttk.Frame):
    def __init__(self, parent):
        super().__init__()

        self.frame = tk.Frame(parent.ttk, bd=2, relief="solid", padx=10, pady=10, width=100)
        self.frame.pack_propagate(False)
        self.frame.grid(padx = 20, pady = 10, row = 1, column=0, sticky='n')
        self.frame['borderwidth'] = 1

        
        def switch():
            
            holder = self.entry.get()
            holder2 = self.entry2.get()
            self.entry.delete(0, '')
            self.entry2.delete(0, '')
            self.entry.insert(0, holder2)
            self.entry2.insert(0, holder)
            pass


    #---------------------------------------------------------------------------------------------------------------------------#

        def load_data(filename):
            stations = []
            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                next(reader)  # Pomija nagłówki
                for row in reader:
                    stations.append(row[0])  # Dodaje tylko nazwy stacji
            return stations

        # Funkcja do aktualizacji listy podpowiedzi
        def update_listbox(data):
            # Usunięcie wszystkich elementów z listbox
            self.listbox.delete(0, tk.END)
            # Dodanie nowych elementów do listbox
            for item in data:
                self.listbox.insert(tk.END, item)

        # Funkcja wywoływana przy każdej zmianie tekstu w Entry
        def on_keyrelease(event):
            self.entry.configure(style = 'quocalcus.TEntry')
            
            self.listbox.grid(padx=10, pady=1, row=2, column=0, sticky="e")
            self.listbox.bind('<<ListboxSelect>>', on_listbox_select)
            # Pobranie tekstu z Entry
            value = self.entry.get().lower().replace(' ','+')
            if value == '':
                data = stations  # Wyświetla wszystkie stacje, gdy pole jest puste
            else:
                data = [item.replace('+',' ') for item in stations if value in item.lower()]

            # Aktualizacja listbox
            update_listbox(data)

        # Funkcja wywoływana przy kliknięciu na element listbox
        def on_listbox_select(event):
            self.switch1['state'] = "enabled"
            # Pobranie indeksu zaznaczonego elementu
            selection = self.listbox.curselection()
            if selection:
                index = selection[0]
                # Pobranie tekstu zaznaczonego elementu
                selected_text = self.listbox.get(index)
                # Wprowadzenie tekstu do Entry
                self.entry.delete(0, tk.END)
                self.entry.insert(0, selected_text)
            self.listbox.grid_remove()
        

        ####################################################################


        # Funkcja do aktualizacji listy podpowiedzi
        def update_listbox2(data):
            # Usunięcie wszystkich elementów z listbox
            self.listbox2.delete(0, tk.END)
            # Dodanie nowych elementów do listbox
            for item in data:
                self.listbox2.insert(tk.END, item)

        # Funkcja wywoływana przy każdej zmianie tekstu w Entry
        def on_keyrelease2(event):
            self.entry2.configure(style = 'quocalcus.TEntry')
            self.listbox2.grid(padx=10, pady=1, row=2, column=2, sticky="e")
            self.listbox2.bind('<<ListboxSelect>>', on_listbox_select2)
            # Pobranie tekstu z Entry
            value = self.entry2.get().lower().replace(' ','+')
            if value == '':
                data = stations  # Wyświetla wszystkie stacje, gdy pole jest puste
            else:
                data = [item.replace('+',' ') for item in stations if value in item.lower()]

            # Aktualizacja listbox
            update_listbox2(data)

        # Funkcja wywoływana przy kliknięciu na element listbox
        def on_listbox_select2(event):
            self.switch1['state'] = "enabled"
            # Pobranie indeksu zaznaczonego elementu
            selection = self.listbox2.curselection()
            if selection:
                index = selection[0]
                # Pobranie tekstu zaznaczonego elementu
                selected_text2 = self.listbox2.get(index)
                # Wprowadzenie tekstu do Entry
                self.entry2.delete(0, tk.END)
                self.entry2.insert(0, selected_text2)
            self.listbox2.grid_remove()
        
        def on_right_click(event):
            self.entry.delete(0, '')

        def on_right_click2(event):
            self.entry2.delete(0, '')


    #---------------------------------------------------------------------------------------------------------------------------#

        def find_data(date):
            var.properties[3] = date.get()
                
        def update():
            var.resultRow = 3
            #print(var.result[5])
            
            
            if var.result[5] !=0:
                for i in range(5):
                    var.result[i].frame1.destroy()
                    
                del var.result
            var.result=[0,0,0,0,0,0,0]
            var.properties[0] = self.entry.get()
            var.properties[1] = self.entry2.get()
            if var.properties[0]=='':
                self.entry.insert(0, 'Pole wymagane')
                self.entry.configure(style = 'danger.TEntry')
                return
            if var.properties[1]=='':
                self.entry2.insert(0, 'Pole wymagane')
                self.entry2.configure(style = 'danger.TEntry')
                return
            if var.properties[2] == 0:
                self.menu1.configure(style='danger.Outline.TMenubutton')
                return
            if var.properties[3] == 0:
                self.cal.configure(style='danger.TCalendar')
                return
            for i in range(5):
                var.result[i] = SearchResult(ttk)
            print(var.properties)

        mystyle = ttk.Style()
        mystyle.configure("quocalcus.Outline.TMenubutton", font=("Tahoma", 20))

        buttonStyle = ttk.Style()
        buttonStyle.configure("quocalcus.Outline.TButton", font=("Tahoma", 20))

        dateStyle = ttk.Style()
        dateStyle.configure("quocalcus.TCalendar", font=("Tahoma", 20))

        entryStyle = ttk.Style()
        entryStyle.configure("quocalcus.TEntry", font=("Tahoma", 20))

        menubuttonStyle = ttk.Style()
        menubuttonStyle.configure('danger.Outline.TMenubutton', font=("Tahoma", 20))

        #---------------------------------------------------------------------------------------------------------------------------#

        
        stations = load_data('Hafas_Codes.csv')

        self.entry = ttk.Entry(self.frame, style='quocalcus.TEntry', width=20, font=("Tahoma", 20))
        self.entry.insert(0,"Skąd jedziemy?")
        self.entry.grid(padx=10, pady=10, row=1, column=0, sticky="e")

        self.listbox = tk.Listbox(self.frame, width=44, height=6,font=("Tahoma", 10))
        # Powiązanie funkcji z zdarzeniem
        self.entry.bind('<KeyRelease>', on_keyrelease)
        self.entry.bind('<Button-3>', on_right_click)
        
        
    #-----------------------------------------------------switch----------------------------------------------------------------------#
        self.switch1 = ttk.Button(self.frame, style="quocalcus.Outline.TButton", text="<>", command=switch)
        self.switch1.grid(padx=10, pady=10, row=1, column=1, sticky="")

        self.switch1['state'] = "disabled"

    #---------------------------------------------------------------------------------------------------------------------------#

        # Przycisk menu do kad jedziemy
        self.entry2 = ttk.Entry(self.frame, style='quocalcus.TEntry', width=20, font=("Tahoma", 20))
        self.entry2.insert(0,"Gdzie jedziemy?")
        self.entry2.grid(padx=10, pady=10, row=1, column=2, sticky="e")
        self.listbox2 = tk.Listbox(self.frame, width=44, height=6,font=("Tahoma", 10))
        # Powiązanie funkcji z zdarzeniem
        self.entry2.bind('<KeyRelease>', on_keyrelease2)
        self.entry2.bind('<Button-3>', on_right_click2)


    #---------------------------------------------------------------------------------------------------------------------------#

        def change1(text):
            #menubuttonStyle.configure('danger.Outline.TMenubutton', font=("Tahoma", 20))
            self.menu1.configure(text=text, style='quocalcus.Outline.TMenubutton')
            var.properties[2] = text
            #parent.label1.config(text=text)

        self.menu1 = ttk.Menubutton(self.frame, style="quocalcus.Outline.TMenubutton", text="00:00")
        self.menu1.grid(padx=10, pady=10, row=1, column=3, sticky="e") 

        # Itemy w menu
        in_menu1 = ttk.Menu(self.menu1)
        item_var = tk.StringVar()
        for x in [f"{hour:02d}:00" for hour in range(24)]:
            in_menu1.add_radiobutton(label=x, variable=item_var, command=lambda x=x: change1(x))
        self.menu1['menu'] = in_menu1

        ##########

        self.cal = ttk.DateEntry(self.frame, style="quocalcus.TCalendar",)
        self.cal.grid(padx=10, pady=10, row=1, column=4, sticky="e")  

        self.sv = tk.StringVar()
        self.sv.trace_add("write", lambda name, index, mode, sv=self.sv: find_data(sv))
        self.cal.entry.configure(textvariable=self.sv)

        ########## Przycisk wyszukiwania
        self.find = ttk.Button(self.frame, style="quocalcus.Outline.TButton", text="Szukaj", command=update)
        self.find.grid(padx=10, pady=10, row=1, column=5, sticky="e")

        #########

class SearchResult(ttk.Frame):
    def __init__(self, parent):
        super().__init__()


        def openWeb(comp):
            if comp == "Szwagropol":
                web.open("https://www.szwagropol.pl/")

        #resultData = ['Company', 'Departure', 'Arrival', 'link', 'price']
        
        resultData = search.search_transport(*var.properties)
        print(resultData)
        
        self.frame1 = tk.Frame( bd=2, relief="solid", padx=10, pady=10, width=1200, height=100)
        self.frame1.grid(padx = 10, pady = 10, row = var.resultRow, column=0, sticky='n')
        self.frame1.grid_propagate(False)
        self.frame1.grid_columnconfigure(0, weight=1)
        self.frame1.grid_rowconfigure(1, weight=0)
        self.frame1['borderwidth'] = 1
        ####
        #
        col = 0
        for i in resultData[var.resultRow-3]:
            self.label1 = ttk.Label(self.frame1 ,text=i, font=("Tahoma", 15))
            if resultData == "No results":
                self.label1.config(bootstyle = 'danger')
            
            self.label1.grid(padx = 10, pady = 10, row = 0, column=col,sticky='n')
            col+=1
        if resultData != "No results":
            self.wabpage = ttk.Button(self.frame1, bootstyle="quocalcus.Outline.TButton", text="Strona", command=lambda: openWeb(var.company))
            self.wabpage.grid(padx=10, pady=10, row=0, column=5, sticky="nes")
        var.resultRow+=1
        """
    

    
        res = [var.company]
        day = 0
        finded = False
        for i in var.dest_list[var.destination]:
            
            if i[0][:2] == var.properties[2][:2]:
                res.extend(i)
                finded = True

                return res
            else:
                day = day + 1
        if day >=24 or finded == False:
            print("No results")
            return "No results"
        """
        


def Labels(label, bus):
    if bus == "Szwagropol":
        all_labels = {
            '(1-5)': ('poniedzialek','wtorek','sroda','czwartek','piatek'),
            '(1-6)': ('poniedzialek','wtorek','sroda','czwartek','piatek', 'sobota'),
            '(1-7)': ('poniedzialek','wtorek','sroda','czwartek','piatek', 'sobota', 'niedziela'),
            '(5-7)': ('piatek', 'sobota', 'niedziela'),
            '(6-7)': ('sobota','niedziela'),
            '(1-5,7)': ('poniedzialek','wtorek','sroda','czwartek','piatek', 'niedziela'),
            '(5)': ('piatek'),
            '(6)': ('sobota'),
            '(7)': ('niedziela')
        }
    elif bus == "Majer":
                all_labels = {
            '(1,7)': ('poniedzialek','wtorek','sroda','czwartek','piatek', 'sobota', 'niedziela'),
            '(5,6,7)': ('piatek', 'sobota', 'niedziela'),
            '(6,7,1)': ('sobota','niedziela','poniedzialek'),
            '(6,7)': ('sobota', 'niedziela'),
            '(5)': ('piatek'),
            '(6)': ('sobota'),
            '(7)': ('niedziela'),
            '(1)': ('poniedzialek'),
        }
    return all_labels[label]

    
class transport:

    def __init__(self):
        self.is_connection = None
        self.start = None
        self.destination = None
        self.day_label = None
        self.page = None
        self.train_name = []
        self.top5_dep_time = []
        self.top5_arr_time = []
        self.top6_dep_time = []
        self.top6_arr_time = []
        self.train_change_city = []


    def szwagropol(self, start, destination, planned_dep_time, day):

        if start  == 'Nowy Sącz' or destination == 'Nowy Sącz':
            self.page = 'https://www.szwagropol.pl/pl/linie-autobusowe/rozklad-jazdy/?rozklad=2&kierunek=6'
        elif start  == 'Zakopane' or destination == 'Zakopane':
            self.page = 'https://www.szwagropol.pl/pl/linie-autobusowe/rozklad-jazdy/?rozklad=1&kierunek=2'

        query = requests.get(self.page)
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
        self.page = 'https://www.majerbus.pl/pl/linia-regularna-zakopane-nowytarg-krakow'
        query = requests.get(self.page)
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

    '''
    def AD(self,start,destination,leave, dates):
        
        self.start = start
        self.destination = destination
        self.leave = leave
        self.date = dates
        
        self.dzien_tyg = ["poniedzialek","wtorek","sroda","czwartek","piatek"]
        
        self.strona = "https://www.busy-krk.pl/slomniki-krakow/"
            
        self.query = requests.get(self.strona)

        self.soup = bs(self.query.content, 'html.parser')

        self.timetable = []

        self.rows = self.soup.find_all('tr')
        self.headers = [header.get_text().strip() for header in self.rows[12].find_all('th')]
        

        for row in self.rows[1:]:
            self.cells = row.find_all('td')
            self.hour = None
            for idx, cell in enumerate(self.cells):
                self.text = cell.get_text().strip()
                if self.text:
                    if self.hour is None:
                        self.hour = self.text
                    else:
                        if idx < len(self.headers):
                            self.day = self.headers[idx]
                            self.timetable.append([self.day, f"{self.hour}:{self.text}"])



        if self.start == "Słomniki":
            self.timetable = [i for i in self.timetable if i[0]][35:60]
        else:
            self.timetable = [i for i in self.timetable if i[0]][10:35]
        
        for i in self.timetable:
           if len(i[1][2:]) > 4:
               x = i[1][5:]
               i[1] = i[1][:4]
               self.timetable.append([i[0],i[1][:2] + x])
            
        for i in self.dzien_tyg:       
            for j in self.timetable:
                if j[0] == "pon. - pt.":
                    self.timetable.append([i,j[1]])
        
        #return self.top5_departures
    
    '''
        
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

        date_link = date.replace('.','')
        hour_link = planned_dep_time.replace(':','')
        zero_link = '0'
        
        if planned_dep_time[:2] != '00' and int(planned_dep_time[:2]) > 10:
            self.page = f'https://bilkom.pl/podroz?basketKey=&carrierKeys=PZ%2CP2%2CP1%2CP5%2CP7%2CP4%2CP9%2CP0%2CO1%2CP3%2CP6%2CP8&trainGroupKeys=G.EXPRESS_TRAINS%2CG.FAST_TRAINS%2CG.REGIONAL_TRAINS&fromStation={start_link}&poczatkowa=A%3D1%40O%3D{start_link}%40X%3D19947423%40Y%3D50067192%40U%3D51%40L%3D{station_code(start_link)}%40B%3D1%40p%3D1716898916%40&toStation={destination_link}&docelowa=A%3D1%40O%3D{destination_link}%40X%3D22006798%40Y%3D50043110%40U%3D51%40L%3D{station_code(destination_link)}%40B%3D1%40p%3D1716898916%40&middleStation1=&posrednia1=&posrednia1czas=&middleStation2=&posrednia2=&posrednia2czas=&data={date_link}{str(int(planned_dep_time[:2])-1)+planned_dep_time[-2:]}&date={date[:2]}%2F{date[3:5]}%2F{date[-4:]}&time={str(int(planned_dep_time[:2])-1)}%3A{planned_dep_time[-2:]}&minChangeTime=10&przyjazd=false&_csrf='
        elif int(planned_dep_time[:2]) <= 10:
            self.page = f'https://bilkom.pl/podroz?basketKey=&carrierKeys=PZ%2CP2%2CP1%2CP5%2CP7%2CP4%2CP9%2CP0%2CO1%2CP3%2CP6%2CP8&trainGroupKeys=G.EXPRESS_TRAINS%2CG.FAST_TRAINS%2CG.REGIONAL_TRAINS&fromStation={start_link}&poczatkowa=A%3D1%40O%3D{start_link}%40X%3D19947423%40Y%3D50067192%40U%3D51%40L%3D{station_code(start_link)}%40B%3D1%40p%3D1716898916%40&toStation={destination_link}&docelowa=A%3D1%40O%3D{destination_link}%40X%3D22006798%40Y%3D50043110%40U%3D51%40L%3D{station_code(destination_link)}%40B%3D1%40p%3D1716898916%40&middleStation1=&posrednia1=&posrednia1czas=&middleStation2=&posrednia2=&posrednia2czas=&data={date_link}{zero_link+str(int(planned_dep_time[:2])-1)+planned_dep_time[-2:]}&date={date[:2]}%2F{date[3:5]}%2F{date[-4:]}&time={str(int(planned_dep_time[:2])-1)}%3A{planned_dep_time[-2:]}&minChangeTime=10&przyjazd=false&_csrf='  
        else:
            self.page = f'https://bilkom.pl/podroz?basketKey=&carrierKeys=PZ%2CP2%2CP1%2CP5%2CP7%2CP4%2CP9%2CP0%2CO1%2CP3%2CP6%2CP8&trainGroupKeys=G.EXPRESS_TRAINS%2CG.FAST_TRAINS%2CG.REGIONAL_TRAINS&fromStation={start_link}&poczatkowa=A%3D1%40O%3D{start_link}%40X%3D19947423%40Y%3D50067192%40U%3D51%40L%3D{station_code(start_link)}%40B%3D1%40p%3D1716898916%40&toStation={destination_link}&docelowa=A%3D1%40O%3D{destination_link}%40X%3D22006798%40Y%3D50043110%40U%3D51%40L%3D{station_code(destination_link)}%40B%3D1%40p%3D1716898916%40&middleStation1=&posrednia1=&posrednia1czas=&middleStation2=&posrednia2=&posrednia2czas=&data={date_link}{hour_link}&date={date[:2]}%2F{date[3:5]}%2F{date[-4:]}&time={hour_link}%3A{planned_dep_time[-2:]}&minChangeTime=10&przyjazd=false&_csrf='
        print(self.page)
        query = requests.get(self.page)
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



            
