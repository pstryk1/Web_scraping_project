import tkinter as tk
import ttkbootstrap as ttk
from bs4 import BeautifulSoup as bs
from lxml import html
import requests
import sys

themes = ('darkly', 'flatly')

#def Maxbus_data(date, hour):


def Maxbus_scrapped():
    page1 = 'https://maxbus.com.pl/rozklad/krakow-zegocina-laskowa-limanowa/'
    query = requests.get(page1)
    scrape = bs(query.text, 'html.parser')
    #body = scrap.body
    tab = scrape.find('tbody')
    #col = tab.find_all('col')
    return tab


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



#class Maxbus_Limanowa:

    #def __init__(self, day_sign, route, dep_time, arr_time):

print(Maxbus_scrapped())