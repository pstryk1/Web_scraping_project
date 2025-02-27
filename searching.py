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

        if len(train.top6_dep_time):
            train.train(start, destination, hour, day)

        szwagropol_data = [['Szwagropol', szwagropol.top5_dep_time[i], szwagropol.top5_arr_time[i], 'Bezpośrednio', szwagropol.page] for i in range(5)]
        
        train_data = []
        counter = 0
        for i in range(6):
            if type(train.train_name[i]) != list:
                train_data.append([train.train_name[i], train.top6_dep_time[i], train.top6_arr_time[i], 'Bezpośrednio', train.page])
            else:
                train_data.append([train.train_name[i], train.top6_dep_time[i], train.top6_arr_time[i], train.train_change_city[counter], train.page])
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

        if len(train.top6_dep_time):
            train.train(start, destination, hour, day)

        szwagropol_data = [['Szwagropol', szwagropol.top5_dep_time[i], szwagropol.top5_arr_time[i], 'Bezpośrednio', szwagropol.page] for i in range(5)]
        majer_data = [['Majer', majer.top5_dep_time[i], majer.top5_arr_time[i], 'Bezpośrednio', majer.page] for i in range(5)]
        
        train_data = []
        counter = 0

        for i in range(6):
            if type(train.train_name[i]) != list:
                train_data.append([train.train_name[i], train.top6_dep_time[i], train.top6_arr_time[i], 'Bezpośrednio', train.page])
            else:
                train_data.append([ train.train_name[i], train.top6_dep_time[i], train.top6_arr_time[i], train.train_change_city[counter], train.page])
                counter += 1

        transport = []
        transport.extend(szwagropol_data)
        transport.extend(majer_data)
        transport.extend(train_data)

        transport = sorted([sorted(transport, key= lambda o: abs(datetime.strptime(hour, '%H:%M') - datetime.strptime(o[1], '%H:%M')))[i] for i in range(6)], key= lambda o: o[1])

    elif (start == 'Kraków Główny' and destination == 'Słomniki') or (destination == 'Kraków Główny' and start == 'Słomniki'):
        
        ad = cs.transport()
        ad.AD(start, destination, hour, day)
        
        train = cs.transport()
        train.train(start, destination, hour, day)

        ad_data = [['AD', ad.top5_dep_time[i], ad.top5_arr_time[i], 'Bezpośrednio', ad.page] for i in range(5)]
        
        train_data = []
        counter = 0
        for i in range(6):
            if type(train.train_name[i]) != list:
                train_data.append([train.train_name[i], train.top6_dep_time[i], train.top6_arr_time[i], 'Bezpośrednio', train.page])
            else:
                train_data.append([ train.train_name[i], train.top6_dep_time[i], train.top6_arr_time[i], train.train_change_city[counter], train.page])
                counter += 1

        transport = []
        transport.extend(ad_data)
        transport.extend(train_data)

        transport = sorted([sorted(transport, key= lambda o: abs(datetime.strptime(hour, '%H:%M') - datetime.strptime(o[1].replace(' ',':'), '%H:%M')))[i] for i in range(6)], key= lambda o: o[1])
        print('gej')
        print(transport)
    else:

        train = cs.transport()
        train.train(start, destination, hour, day)

        if len(train.top6_dep_time):
            train.train(start, destination, hour, day)

        transport = []
        counter = 0

        if len(train.top6_dep_time) != 0:
            for i in range(6):
                if type(train.train_name[i]) != list:
                    transport.append([train.train_name[i], train.top6_dep_time[i], train.top6_arr_time[i], 'Bezpośrednio', train.page])
                else:
                    transport.append([train.train_name[i], train.top6_dep_time[i], train.top6_arr_time[i], train.train_change_city[counter], train.page])
                    counter += 1

    return transport