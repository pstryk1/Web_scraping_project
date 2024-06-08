from bs4 import BeautifulSoup as bs
import requests

list_range = ['A', 'B', 'C', 'Ć', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'Ł', 'M', 'N', 'O', 'P', 'R', 'S', 'Ś', 'T', 'U', 'W', 'Z', 'Ź', 'Ż']
hafas_list = []

for i in list_range:
    page = f'https://www.bazakolejowa.pl/index.php?dzial=stacje&st={i}'
    query = requests.get(page)
    scrape = bs(query.text, 'lxml')

    links = [i.a['href'] for i in scrape.find_all('span', style='white-space: nowrap')]

    for j in links:
        page = f'https://www.bazakolejowa.pl/{j}'
        query = requests.get(page)
        scrape = bs(query.text, 'lxml')

        stations = [i.a['href'] for i in scrape.find_all('span', class_='linka')]
        
        for k in stations:
            page = f'https://www.bazakolejowa.pl/{k}'
            query = requests.get(page)
            scrape = bs(query.text, 'lxml')

            staction_name = scrape.find('div', class_='tytul').text

            if len(staction_name.split()) > 1:
                name = ''
                for i in staction_name.split():
                    if name != '':
                        name = name + '+' + i
                    else:
                        name = i
                staction_name = name

            hafas = scrape.find('td', id='wyp11Text')
            
            if hafas != None:
                hafas_list = hafas.text.split()
                for m in hafas_list:
                    if 'HAFAS' in m:
                        hafas_code = m[6:]
                        with open(f'Hafas_Codes.csv', 'a' , encoding= 'utf8') as file:
                            file.writelines(f'{staction_name};{hafas_code}\n')
                        break


