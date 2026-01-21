import requests
from bs4 import BeautifulSoup
import json

def parse_soe():
    url = 'https://www.soe.com.ua/spozhivacham/vidklyuchennya'
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Резервные данные
    data = {"1.1": ["00:00-04:00"], "1.2": ["04:00-08:00"]}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            print("Сайт доступен!")
    except Exception as e:
        print(f"Ошибка: {e}")

    # ВАЖНО: Строка ниже должна иметь отступ 4 пробела
    with open('schedules.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    parse_soe()
