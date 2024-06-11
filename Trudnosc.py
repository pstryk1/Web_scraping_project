import classes as cs

with open(f'Hafas_Codes.csv', 'r' , encoding= 'utf8') as file:
    csv = file.readlines()

new_csv = []
for i in csv:
    i = i.strip().split(';')
    new_csv.append(i)

licznik = 0
for i in new_csv:

    if licznik == 40:
        exit()

    transport = cs.transport()
    try:
        transport.train(i[0], 'Warszawa Centralna', '12:00', '12.06.2024')
        name = transport.all_results[0][0][-1]
    except:
        try:
            transport.train(i[0], 'Kraków Główny', '12:00', '12.06.2024')
            name = transport.all_results[0][0][-1]
        except IndexError:
            try:
                transport.train(i[0], 'Rzeszów Główny', '12:00', '12.06.2024')
                name = transport.all_results[0][0][-1]
            except:
                try:
                    transport.train(i[0], 'Poznań Główny', '12:00', '12.06.2024')
                    name = transport.all_results[0][0][-1]
                except:
                    try:
                        transport.train(i[0], 'Gdańsk Główny', '12:00', '12.06.2024')
                        name = transport.all_results[0][0][-1]
                    except:
                        transport.train(i[0], 'Lublin Główny', '12:00', '12.06.2024')
                        name = transport.all_results[0][0][-1]
    licznik += 1


    if i[0] == name:
        with open(f'Hafas_Codes_edited.csv', 'a' , encoding= 'utf8') as file2:
            file2.writelines(f'{i[0]};{i[1]}\n')