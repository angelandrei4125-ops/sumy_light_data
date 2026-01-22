import requests
import json
import re

def parse_soe():
    # Тот самый скрытый URL, куда сайт обращается при нажатии на очередь
    api_url = 'https://www.soe.com.ua/spozhivacham/vidklyuchennya/get-gpv-data'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest', # Сообщаем сайту, что это AJAX запрос
        'Referer': 'https://www.soe.com.ua/spozhivacham/vidklyuchennya/grafik-pogodinnikh-vidklyuchen',
    }

    queues = ["1.1", "1.2", "2.1", "2.2", "3.1", "3.2", "4.1", "4.2", "5.1", "5.2", "6.1", "6.2"]
    final_data = {}

    for q in queues:
        try:
            # Отправляем POST, как будто мы выбрали очередь в выпадающем списке
            response = requests.post(api_url, data={'queue': q}, headers=headers, timeout=15)
            
            if response.status_code == 200:
                html_text = response.text
                
                # Ищем все интервалы типа 06:00-10:00 или 06:00 - 10:00
                matches = re.findall(r'(\d{2}[:\.]\d{2})\s*-\s*(\d{2}[:\.]\d{2})', html_text)
                
                # Собираем только уникальные интервалы в формате 00:00-00:00
                times = sorted(list(set([f"{m[0].replace('.', ':')}-{m[1].replace('.', ':')}" for m in matches])))
                
                if times:
                    final_data[q] = times
                    print(f"Очередь {q}: Найдено {len(times)} периодов")
                else:
                    final_data[q] = [] 
                    print(f"Очередь {q}: График не найден в ответе")
            else:
                print(f"Очередь {q}: Ошибка сервера {response.status_code}")
                
        except Exception as e:
            print(f"Ошибка на {q}: {e}")

    # Сохраняем результат
    if final_data:
        with open('schedules.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)
        print("--- Файл schedules.json обновлен! ---")

if __name__ == "__main__":
    parse_soe()
