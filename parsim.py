from bs4 import BeautifulSoup
import requests
import csv

CSV = 'kivano_nout.csv'
HOST = 'https://www.kivano.kg/'
URL = 'https://www.kivano.kg/noutbuki'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0'}


def get_html(url, params=''):
    respose = requests.get(URL, headers=HEADERS, params=params, verify=False)
    print(respose.content)
    return respose


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_='item product_listbox oh')
    comps = []

    for item in items:
        comps.append({
            'title': item.find('div', class_='listbox_title oh').find('a').get_text(strip=True),
            'price': item.find('div', class_='listbox_price text-center').get_text(strip=True),
            'link': HOST + item.find('div', class_='listbox_img pull-left').find('img').get('src')
        })

    return comps


def save(items, path):
    with open(path, 'a') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Цена', 'Ссылка'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['link']])


def parser():
    PAGENATOR = input("Введите номер страницы: ")
    PAGENATOR = int(PAGENATOR.strip())
    html = get_html(URL)
    if html.status_code == 200:
        new_list = []
        for page in range(1, PAGENATOR):
            print(f"Страница №{page} готова")
            html = get_html(URL, params={'page': page})
            new_list.extend(get_content(html.text))
        save(new_list, CSV)
        print("Парсинг готов")
    else:
        print('error')


parser()
