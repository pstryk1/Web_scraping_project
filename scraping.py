import tkinter as tk
import ttkbootstrap as ttk
from bs4 import BeautifulSoup as bs
from lxml import html
import requests
import sys
from datetime import datetime
import classes as cs


def search_transport(start, destination, hour, day):

    def day_name(day):
        day = datetime.strptime(day, '%d.%m.%Y')
        day_name = datetime.strftime(day, '%A')
        return day_name

    if (start == 'Nowy Sącz' and destination == 'Kraków Główny') or (destination == 'Nowy Sącz' and start == 'Kraków Główny'):

        szwagropol = cs.transport()
        szwagropol.szwagropol(start, destination, hour, day_name(day))

        train = cs.transport()
        train.train(start, destination, hour, day)

        szwagropol_data = [['Szwagropol', szwagropol.top5_dep_time[i], szwagropol.top5_arr_time[i]] for i in range(5)]
        
        train_data = []
        counter = 0
        for i in range(6):
            if type(train.train_name[i]) != list:
                train_data.append([train.train_name[i], train.top6_dep_time[i], train.top6_arr_time[i]])
            else:
                train_data.append([train.train_name[i], train.top6_dep_time[i], train.top6_arr_time[i], train.train_change_city[counter]])
                counter += 1

        transport = []
        transport.extend(szwagropol_data)
        transport.extend(train_data)

        transport = sorted([sorted(transport, key= lambda o: abs(datetime.strptime(hour, '%H:%M') - datetime.strptime(o[1], '%H:%M')))[i] for i in range(6)], key= lambda o: o[1])

    elif (start == 'Zakopane' and destination == 'Kraków Główny') or (destination == 'Zakopane' and start == 'Kraków Główny'):

        szwagropol = cs.transport()
        szwagropol.szwagropol(start, destination, hour, day_name(day))

        majer = cs.transport()
        majer.majer(start, destination, hour, day_name(day))

        train = cs.transport()
        train.train(start, destination, hour, day)

        szwagropol_data = [['Szwagropol', szwagropol.top5_dep_time[i], szwagropol.top5_arr_time[i]] for i in range(5)]
        majer_data = [['Majer', majer.top5_dep_time[i], majer.top5_arr_time[i]] for i in range(5)]
        
        train_data = []
        counter = 0
        for i in range(6):
            if type(train.train_name[i]) != list:
                train_data.append([train.train_name[i], train.top6_dep_time[i], train.top6_arr_time[i]])
            else:
                train_data.append([ train.train_name[i], train.top6_dep_time[i], train.top6_arr_time[i], train.train_change_city[counter]])
                counter += 1

        transport = []
        transport.extend(szwagropol_data)
        transport.extend(majer_data)
        transport.extend(train_data)

        transport = sorted([sorted(transport, key= lambda o: abs(datetime.strptime(hour, '%H:%M') - datetime.strptime(o[1], '%H:%M')))[i] for i in range(6)], key= lambda o: o[1])

    elif (start == 'Słomniki' and destination == 'Kraków Główny') or (destination == 'Słomniki' and start == 'Kraków Główny'):

        AD = cs.transport()
        transport = AD.AD(start, destination, hour, day)

        #train = cs.transport()
        #train.train(start, destination, hour, day)
        
    else:

        train = cs.transport()
        train.train(start, destination, hour, day)        

        transport = []
        counter = 0

        if len(train.top6_dep_time) != 0:
            for i in range(6):
                if type(train.train_name[i]) != list:
                    transport.append([train.train_name[i], train.top6_dep_time[i], train.top6_arr_time[i]])
                else:
                    transport.append([train.train_name[i], train.top6_dep_time[i], train.top6_arr_time[i], train.train_change_city[counter]])
                    counter += 1
        else:
            raise ValueError('\nNie mozna wyszukac trasy z przeszlosci\n')

    return transport



#print(search_transport('Nowy Sącz', 'Kraków Główny', '12:00', '30.06.2024'))
#print(search_transport('Zakopane', 'Kraków Główny', '10:00', '31.05.2024'))
print(search_transport('Kraków Główny', 'Słomniki', '11:00', '2024-06-11'))

'''
ab = cs.transport()

ab.train('Kraków Główny', 'Niedźwiedź', '10:00', '2024-06-11')

print(ab.start)
print(ab.destination)
print(ab.top6_dep_time)
print(ab.top6_arr_time)

'''
