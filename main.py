import requests
from bs4 import BeautifulSoup
import json
import re


def get_price_sportmaraphon(url: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    price, discount_price = 0, 0
    mess = 'Успешно получена цена'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        script_tag = soup.find('script', text=re.compile(r'"price":'))
        if script_tag:
            json_text = re.search(r'\{.*"price":.*\}', script_tag.string).group()
            data = json.loads(json_text)
            price = data.get('price', 'Цена не найдена')
            discount_price = data.get('discountPrice', 'Скидочная цена не найдена')
            print('Цена товара:', price)
            print('Скидочная цена товара:', discount_price)
        else:
            mess = 'Не удалось найти нужные данные на странице'
    else:
        mess = f'Не удалось получить страницу, статус код: {response.status_code}'
    return min(price, discount_price), mess


def get_price_trialsport(url: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    price, discount_price = 0, 0
    mess = 'Успешно получена цена'

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Поиск скрипта, содержащего нужные данные
        script_tag = soup.find('script', string=re.compile(r'var eventParams = \{'))
        if script_tag and script_tag.string:
            # Извлечение JSON-строки из JavaScript
            json_text_match = re.search(r'var eventParams = (\{.*?\});', script_tag.string, re.DOTALL)
            if json_text_match:
                json_text = json_text_match.group(1)
                try:
                    # Парсинг JSON
                    data = json.loads(json_text)

                    # Извлечение информации о продуктах
                    products = data.get('products', [])
                    if products:
                        product = products[0]
                        price = product.get('price', 0)
                        discount_price = product.get('price_old', 0)
                        print('Цена товара:', price)
                        print('Старая цена товара:', discount_price)
                    else:
                        mess = 'Не удалось найти информацию о продуктах на странице'
                except json.JSONDecodeError:
                    mess = 'Ошибка при разборе JSON'
            else:
                mess = 'Не удалось извлечь JSON из JavaScript'
        else:
            mess = 'Не удалось найти нужные данные на странице'
    else:
        mess = f'Не удалось получить страницу, статус код: {response.status_code}'

    return min(price, discount_price), mess


def get_price_kant(url: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    price = 0
    mess = 'Успешно получена цена'

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Поиск скрипта, содержащего нужные данные
        script_tag = soup.find('script', string=re.compile(r'"offers":\[\{.*\}\]'))
        if script_tag and script_tag.string:
            # Извлечение JSON-строки из JavaScript
            json_text_match = re.search(r'(\{.*"offers":\[\{.*\}\].*\})', script_tag.string, re.DOTALL)
            if json_text_match:
                json_text = json_text_match.group(1)
                try:
                    # Парсинг JSON
                    data = json.loads(json_text)

                    # Извлечение информации о предложениях
                    offers = data.get('offers', [])
                    if offers:
                        # Предполагаем, что цена одинаковая для всех предложений
                        price = offers[0].get('price', 0)
                        print('Цена товара:', price)
                    else:
                        mess = 'Не удалось найти информацию о предложениях на странице'
                except json.JSONDecodeError:
                    mess = 'Ошибка при разборе JSON'
            else:
                mess = 'Не удалось извлечь JSON из JavaScript'
        else:
            mess = 'Не удалось найти нужные данные на странице'
    else:
        mess = f'Не удалось получить страницу, статус код: {response.status_code}'

    return price, mess


def get_price_splav(url: str):
    price = 0
    mess = 'Успешно получена цена'

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Поиск скрипта с JSON-LD данными
        script_tag = soup.find('script', {'type': 'application/ld+json'})

        if script_tag and script_tag.string:
            try:
                data = json.loads(script_tag.string)

                # Поиск блока "offers" и извлечение цены
                for item in data.get('@graph', []):
                    if item.get('@type') == 'Product':
                        offers = item.get('offers', [])
                        if offers:
                            price = offers[0].get('price', 0)
                            break

                if price:
                    print('Цена товара:', price)
                else:
                    mess = 'Не удалось найти цену в данных'
            except json.JSONDecodeError:
                mess = 'Ошибка при разборе JSON'
        else:
            mess = 'Не удалось найти нужные данные на странице'
    else:
        mess = f'Не удалось получить страницу, статус код: {response.status_code}'

    return price, mess

