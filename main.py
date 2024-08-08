import requests
from bs4 import BeautifulSoup
import json
import re

def get_price_sport_maraphon(url:str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    price, discount_price=0,0
    mess='Успешно получена цена'
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
            mess='Не удалось найти нужные данные на странице'
    else:
        mess=f'Не удалось получить страницу, статус код: {response.status_code}'
    return min(price,discount_price), mess

print(get_price_sport_maraphon('https://sport-marafon.ru/catalog/muzhskie-uteplennye-kurtki-i-pukhovki/kurtka-muzhskaya-sivera-bekhterets-chili/'))
