from tkinter import *
from ttkbootstrap import Style

root = Tk()
root.geometry("200x200")  # Ustawienie rozmiaru okna na 100x100 pikseli

# Inicjalizacja stylu
style = Style(theme='darkly')

# Główny kontener siatki
frame = Frame(root, bg="black")  # Ustawienie koloru tła na czarny
frame.pack(fill="both", expand=True)

# Ustawienie dwóch kolumn i wyśrodkowanie
frame.columnconfigure((0, 1), weight=1)  # Ustawienie wag dla obu kolumn
frame.rowconfigure(0, weight=1)  # Ustawienie wagi dla wiersza

# Utworzenie obiektów typu Frame z czerwonym tłem
frame1 = Button(frame, bg="red")  # Ustawienie koloru tła na czerwony
frame1.grid(row=0, column=0, padx=5, pady=5, sticky="n")  # Ustawienie pierwszego ramki w lewej kolumnie

frame2 = Frame(frame, bg="red")  # Ustawienie koloru tła na czerwony
frame2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")  # Ustawienie drugiego ramki w prawej kolumnie

root.mainloop()




