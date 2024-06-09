import tkinter as tk
import ttkbootstrap as ttk
from bs4 import BeautifulSoup as bs
from lxml import html
import requests
import sys
from datetime import datetime
import classes as cs
import variables as var

url = "https://bilkom.pl/"
response = requests.get(url)
soup = bs(response.text, "html.parser")

# Find all divs with class 'value' and extract their text
for i in range(160):
    try:
        pm10_values = [i.text for i in soup.find_all("label", class_="control-label")]
        print(f"{pm10_values}")
    except:
        print("blokada")