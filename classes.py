import tkinter as tk
import ttkbootstrap as ttk
from bs4 import BeautifulSoup as bs
from lxml import html
import requests
import sys
from datetime import date
import variables as var

themes = ('darkly', 'flatly')
current_theme= 0

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



class Fullscreen_Window:
    seldate = 0

    def __init__(self):
        super().__init__()
        


        self.ttk = ttk.Window(themename=themes[current_theme])
        self.ttk.title("QuoCalCus - znajdź swoj cel")
        self.ttk.attributes("-topmost", True)
        #self.tk.geometry("{0}x{1}+0+0".format(self.tk.winfo_screenwidth(), self.tk.winfo_screenheight()))
        self.ttk.state('zoomed')

        self.frame = tk.Frame(self.ttk, height=100, width=500,  bd=2, relief="groove", padx=10, pady=10)
        self.frame.pack(padx=20, pady=20)
        Search_settings(self)

        #frame1 = ttk.Button(self.frame)  # Ustawienie koloru tła na czerwony
        #frame1.grid(row=0, column=0, padx=100, pady=100, sticky="nesw")
        
        #self.frame.config(background='#ff0000')
        #self.frame.columnconfigure(0, weight=1) 
        #self.frame.rowconfigure(0, weight=1)
        #




        #self.ttk.pack_propagate()
        



        #self.columnconfigure(0, weight=1)  # Ustawienie obu kolumn na wagę 1
        #self.columnconfigure(1, weight=1)
        #self.rowconfigure(0, weight=1)
        #frame1 = ttk.Button(self.frame)  # Ustawienie koloru tła na czerwony
        #frame1.grid(row=0, column=0, padx=100, pady=100, sticky="nesw")

        

        #self.napis = ttk.Label(text='')
        #self.napis.grid(row=1, column=6, )
        #self.label1 = ttk.Label(text='')
        #self.label1.grid(row=1, column=7, padx=20, pady=20)
        

        
        
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
        self.state = not self.state  # Just toggling the boolean
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
        edit_text = tk.Text(height=height, width=width, font=("Arial", 12), bd=2, relief="groove", padx=10, pady=10)
        edit_text.grid(r, c) #expand=False, fill="both"
        return edit_text.get("1.0", "end-1c")  

    def toggle_button(self, text, r, c, px, py):

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
        toggle.grid(padx = px, pady = py, row = r, column=c)

        


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
        

class Search_settings(ttk.Frame):
    def __init__(self, parent):
        super().__init__()


        #self.columnconfigure(0, weight=1)  # Ustawienie obu kolumn na wagę 1
        #self.columnconfigure(1, weight=1)
        #self.rowconfigure(0, weight=1)
        #self.frame1 = ttk.Button(parent.frame)  # Ustawienie koloru tła na czerwony
        #self.frame1.grid(row=0, column=0, padx=100, pady=100, sticky="nesw")

        """
        #self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.config()
        self.columnconfigure(0, weight=1)  # Ustawienie obu kolumn na wagę 1
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid()
        """

        # Przycisk menu
        hours = [f"{hour:02d}:00" for hour in range(24)]


        def change2(text):
            self.menu2.configure(text=text)
            #parent.label1.config(text=text)

        self.menu2 = ttk.Menubutton(parent.frame, bootstyle=themes[current_theme], text="Cel")
        self.menu2.grid(padx=10, pady=10, row=0, column=0, sticky="e", columnspan=1)  # Wyrównanie do środka poziomo

        # Itemy w menu
        in_menu2 = ttk.Menu(self.menu2)
        item_var = tk.StringVar()  # Utwórz zmienną dla opcji
        for x in ('Nowy Targ', "Nowy Sącz", "Słomniki"):
            in_menu2.add_radiobutton(label=x, variable=item_var, command=lambda x=x: change2(x))
        self.menu2['menu'] = in_menu2



        def change1(text):
            self.menu1.configure(text=text)
            #parent.label1.config(text=text)

        self.menu1 = ttk.Menubutton(parent.frame, bootstyle=themes[current_theme], text="00:00")
        self.menu1.grid(padx=10, pady=10, row=0, column=1, sticky="e", columnspan=1)  # Wyrównanie do środka poziomo

        # Itemy w menu
        in_menu1 = ttk.Menu(self.menu1)
        item_var = tk.StringVar()  # Utwórz zmienną dla opcji
        for x in hours:
            in_menu1.add_radiobutton(label=x, variable=item_var, command=lambda x=x: change1(x))
        self.menu1['menu'] = in_menu1

        self.cal = ttk.DateEntry(parent.frame, bootstyle=themes[current_theme])
        self.cal.grid(padx=10, pady=10, row=0, column=2, sticky="e")  # Wyrównanie do środka poziomo

        self.sv = tk.StringVar()
        self.sv.trace_add("write", lambda name, index, mode, sv=self.sv: self.label_update(sv))
        self.cal.entry.configure(textvariable=self.sv)
        









#class Maxbus_Limanowa:

    #def __init__(self, day_sign, route, dep_time, arr_time):

print(Szwagropol('ZAK'))