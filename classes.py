import tkinter as tk
import ttkbootstrap as ttk
from bs4 import BeautifulSoup as bs
from lxml import html
import requests
import sys
from datetime import date
import variables as var

themes = ('darkly', 'flatly')


def Labels(label, bus):
    if bus == "Szwagropol":
        all_labels = {
            '(1-5)': 'Pn-Pt',
            '(1-6)': 'Pn-Sb',
            '(5-7)': 'Pt-Nd',
            '(6-7)': 'Sb-Nd',
            '(1-5,7)': 'Pn-Pt +Nd',
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

def Szwagropol(location):
    if location == 'NS':
        page = 'https://www.szwagropol.pl/pl/linie-autobusowe/rozklad-jazdy/?rozklad=2&kierunek=6'
    elif location == 'ZAK':
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
                    data_3.append(data_4)
                    label = 'Pn-Nd'
                    data_4 = []
                    data_4.append(j[:5])

        data_4.append(label)
        data_3.append(data_4)
        data_2.append(data_3)

    return data_2



class FullscreenWindow:

    def __init__(self):
        super().__init__()
        
        self.ttk = ttk.Window(themename=themes[0])
        self.ttk.title("QuoCalCus - znajdź swoj cel")
        self.ttk.attributes("-topmost", True)
        #self.tk.geometry("{0}x{1}+0+0".format(self.tk.winfo_screenwidth(), self.tk.winfo_screenheight()))
        self.ttk.state('zoomed')
        self.current_theme= 0
        self.toggle_button()
        self.frame = tk.Frame(self.ttk,   bd=2, relief="solid", padx=10, pady=10)#ta ramka jest przeklęta i za chiny nie chce sie przestawić na prawo
        #self.frame.pack(padx=20, pady=20)
        self.frame.grid(padx = 10, pady = 10, row = 1, column=0, sticky='ne')

        self.label1 = ttk.Label(text='Wyniki wyszukiwania')
        #self.label1.pack(padx=20, pady=20)
        self.label1.grid(padx = 10, pady = 10, row = 2, column=0,sticky='n')
        
        SearchSettings(self)
        

        #frame1 = ttk.Button(self.frame)  # Ustawienie koloru tła na czerwony
        #frame1.grid(row=0, column=0, padx=100, pady=100, sticky="nesw")
        #self.frame.config(background='#ff0000')
        #self.frame.columnconfigure(0, weight=1) 
        #self.frame.rowconfigure(0, weight=1)
        #self.ttk.pack_propagate()
        #self.columnconfigure(0, weight=1)  # Ustawienie obu kolumn na wagę 1
        #self.columnconfigure(1, weight=1)
        #self.rowconfigure(0, weight=1)
        #frame1 = ttk.Button(self.frame)  # Ustawienie koloru tła na czerwony
        #frame1.grid(row=0, column=0, padx=100, pady=100, sticky="nesw")
        #self.napis = ttk.Label(text='')
        #self.napis.grid(row=1, column=6, )
        
        #self.find_button(1, 4, 20, 20, label1)
        #self.date_button(1, 5, 20, 20, label1)
        #mainScreen.edit_text(5, 100)
        #mainScreen.edit_text(5, 100)
        #mainScreen.toggle_button("przycisk")
        #self.choose_date(1, 2, 20, 20)

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
        edit_text.grid(r, c) #expand=False, fill="both"
        return edit_text.get("1.0", "end-1c")  

    def toggle_button(self):
        def bfun():
            self.ttk.style.theme_use(themes[var1.get()])
            self.toggle.configure(text=themes[var1.get()].capitalize())
            #self.frame.style.theme_use(themes[var1.get()])

        var1 = ttk.IntVar()
        self.toggle = ttk.Checkbutton(
            bootstyle = "danger, round-toggle",
            text = "Dark",
            variable=var1, 
            onvalue = 1, 
            offvalue=0,
            command=bfun)
        self.toggle.grid(padx = 10, pady = 10, row = 0, column=0, sticky='ne')
        #self.toggle.pack(padx = 10, pady = 10, side=("right", 'top'))

    """
    def choose_date(self, r, c, px, py):
          # Tworzymy StringVar dla daty

        # Funkcja wywoływana przy aktualizacji wartości pola tekstowego
        def update_date(event):
            var.data = event.get()
            
    def find_button(self, r, c, px, py, mylabel):
        def update_label():
            #selected_date = self.cal.get_date()
            #self.label.config(text="Selected Date: " + var.data)
            print(var.data)
            

        button = ttk.Button(text="Find Date", command=update_label)
        button.grid(padx=px, pady=py, row=r, column=c)

    def date_button(self, r, c, px, py, mylabel):
        def update_label():
            #selected_date = self.cal.get_date()
            #self.label.config(text="Selected Date: " + var.data)
            napis = ttk.Label(text=var.data)
            napis.grid(row=7, column=2)
            

        button = ttk.Button(text="data", command=update_label())
        button.grid(padx=px, pady=py, row=r, column=c)
        """
        

class SearchSettings(ttk.Frame):
    def __init__(self, parent):
        super().__init__()
        parent.frame['borderwidth'] = 1
        
        #parent.frame['padding'] = (5,10,5,10)
        
        def switch():
            holder = var.properties[0]
            var.properties[0] = var.properties[1]
            var.properties[1] = holder
            self.menu2.configure(text=var.properties[0])
            self.menu3.configure(text=var.properties[1])
            pass

        def find_data(date):
            var.properties[3] = date.get()
            
        def update():
            var.resultRow = 3
            if var.res1 != 0:
                del var.res1
            print(f"2: {var.properties}")

            if type(var.properties[2]) == str:
                
                var.res1 = SearchResult(parent)
                var.resultRow +=1
                res2= SearchResult(parent)

        ##########

        # Przycisk menu zkad jedziemy
        hours = [f"{hour:02d}:00" for hour in range(24)]
        def change2(text):
            self.menu2.configure(text=text)
            var.properties[0] = text
            if text != "Kraków":
                self.menu3.configure(text="Kraków")
                var.properties[1] = "Kraków"
                self.menu3['state'] = "disabled"
            else:
                self.menu3['state'] = "enable"

        
        mystyle = ttk.Style()
        mystyle.configure("darkly.Outline.TButton", font=("Monsterrat", 18))
            

        self.menu2 = ttk.Menubutton(parent.frame, bootstyle=themes[parent.current_theme], text="Z kąd jedziemy?", width=30)
        self.menu2.grid(padx=10, pady=10, row=1, column=0, sticky="e", columnspan=1)

        # Itemy w menu
        in_menu2 = ttk.Menu(self.menu2)
        item_var2 = tk.StringVar() 
        for x in ('Kraków', 'Nowy Targ', "Nowy Sącz", "Słomniki", 'Zakopane'):
            in_menu2.add_radiobutton(label=x, variable=item_var2, command=lambda x=x: change2(x))
        self.menu2['menu'] = in_menu2
        #########

        self.switch1 = ttk.Button(parent.frame, bootstyle=themes[parent.current_theme], text="<>", command=switch)
        self.switch1.grid(padx=10, pady=10, row=1, column=1, sticky="e")

        self.switch1['state'] = "disabled"

        #########

         # Przycisk menu do kad jedziemy
        hours = [f"{hour:02d}:00" for hour in range(24)]
        def change3(text):
            self.menu3.configure(text=text)
            self.switch1['state'] = "enable"
            var.properties[1] = text
        
        mystyle = ttk.Style()
        mystyle.configure("darkly.Outline.TButton", font=("Monsterrat", 18))
            

        self.menu3 = ttk.Menubutton(parent.frame, bootstyle=themes[parent.current_theme], text="Dokąd jedziemy?", width=30)
        self.menu3.grid(padx=10, pady=10, row=1, column=2, sticky="e", columnspan=1)

        # Itemy w menu
        in_menu3 = ttk.Menu(self.menu2)
        item_var3 = tk.StringVar() 
        for x in ('Kraków', 'Nowy Targ', "Nowy Sącz", "Słomniki", 'Zakopane'):
            in_menu3.add_radiobutton(label=x, variable=item_var3, command=lambda x=x: change3(x))
        self.menu3['menu'] = in_menu3

        ##########

        def change1(text):
            self.menu1.configure(text=text)
            var.properties[2] = text
            #parent.label1.config(text=text)

        self.menu1 = ttk.Menubutton(parent.frame, bootstyle=themes[parent.current_theme], text="00:00")
        self.menu1.grid(padx=10, pady=10, row=1, column=3, sticky="e", columnspan=1) 

        # Itemy w menu
        in_menu1 = ttk.Menu(self.menu1)
        item_var = tk.StringVar()
        for x in hours:
            in_menu1.add_radiobutton(label=x, variable=item_var, command=lambda x=x: change1(x))
        self.menu1['menu'] = in_menu1

        ##########

        self.cal = ttk.DateEntry(parent.frame, bootstyle=themes[parent.current_theme])
        self.cal.grid(padx=10, pady=10, row=1, column=4, sticky="e")  

        self.sv = tk.StringVar()
        self.sv.trace_add("write", lambda name, index, mode, sv=self.sv: find_data(sv))
        self.cal.entry.configure(textvariable=self.sv)

        ##########

        self.find = ttk.Button(parent.frame, bootstyle=themes[parent.current_theme], text="Szukaj", command=update)
        self.find.grid(padx=10, pady=10, row=1, column=5, sticky="e")

        #########
        #cbvalues = ['option 1', 'option 2', 'option 3']
        #self.cb = ttk.Combobox(parent.frame, bootstyle='succes', values=cbvalues)
        #self.cb.grid(padx=10, pady=10, row=1, column=6, sticky="e")

class SearchResult(ttk.Frame):
    def __init__(self, parent):
        super().__init__()
        resultData = ['Company', 'Departure', 'Arrival', 'link', 'price']
        resultData = self.navigate()

        self.frame1 = tk.Frame(  bd=2, relief="solid", padx=10, pady=10)
        #self.frame.pack(padx=20, pady=20)
        self.frame1.grid(padx = 10, pady = 10, row = var.resultRow, column=0, sticky='n')
        ####
        #
        for i in resultData:
            self.label1 = ttk.Label(self.frame1 ,text=i)
            if resultData == "No results":
                self.label1.config(bootstyle = 'warning')
            #self.label1.pack(padx=20, pady=20)
            self.label1.grid(padx = 10, pady = 10, row = 0, column=resultData.index(i),sticky='ne')

    def navigate(self):
        #nawigator po zawiłych listach mateusza
        if var.properties[1] == "Zakopane":
            var.relation=0
            var.destination = 1
            var.dest_list = Szwagropol('ZAK')
            var.company = "Szwagropol"
        elif var.properties[1] == "Nowy Sącz":
            var.relation=0
            var.destination = 1
            var.dest_list = Szwagropol('NS')
            var.company = "Szwagropol"
        elif var.properties[1] == "Kraków":
            var.relation=1
            if var.properties[0] == "Zakopane":
                var.destination = 0
                var.dest_list = Szwagropol('ZAK')
            elif var.properties[0] == "Nowy Sącz":
                var.destination = 0
                var.dest_list = Szwagropol('NS')
            var.company = "Szwagropol"

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
            


#class Maxbus_Limanowa:

    #def __init__(self, day_sign, route, dep_time, arr_time):

#print(Szwagropol('ZAK'))
#print(Maxbus_scrapped())