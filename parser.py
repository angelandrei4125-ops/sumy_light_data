import requests
import json

def parse_soe():
    # URL, по которому сайт реально получает данные для графиков
    api_url = 'https://www.soe.com.ua/spozhivacham/vidklyuchennya/get-gpv-data'
    
    # Список всех очередей, которые нам нужны
    queues = ["1.1", "1.2", "2.1", "2.2", "3.1", "3.2", "4.1", "4.2", "5.1", "5.2", "6.1", "6.2"]
    final_data = {}

    for q in queues:
        try:
            # Отправляем запрос имитируя выбор очереди
            response = requests.post(api_url, data={'queue': q}, timeout=10)
            if response.status_code == 200:
                # Здесь мы будем получать HTML-кусок с текстом про время
                # Для начала просто сохраним, что очередь обработана
                # В будущем тут добавим поиск текста "с 00:00 до 02:00"
                final_data[q] = ["Данные обновлены"] 
            print(f"Очередь {q} обработана")
        except Exception as e:
            print(f"Ошибка на очереди {q}: {e}")

    # Записываем всё в наш файл
    with open('schedules.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    parse_soe()
