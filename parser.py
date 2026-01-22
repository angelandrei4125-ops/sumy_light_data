import requests
import json
import re

def parse_soe():
    api_url = 'https://www.soe.com.ua/spozhivacham/vidklyuchennya/get-gpv-data'
    # Добавляем заголовки, чтобы сайт не блокировал запрос
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    queues = ["1.1", "1.2", "2.1", "2.2", "3.1", "3.2", "4.1", "4.2", "5.1", "5.2", "6.1", "6.2"]
    final_data = {}

    for q in queues:
        try:
            response = requests.post(api_url, data={'queue': q}, headers=headers, timeout=15)
            if response.status_code == 200:
                html_content = response.text
                
                # Ищем время в разных форматах (00:00-04:00 или 00.00-04.00)
                times = re.findall(r'(\d{2}[:\.]\d{2})\s*-\s*(\d{2}[:\.]\d{2})', html_content)
                
                # Чистим данные (заменяем точки на двоеточия для приложения)
                formatted_times = [f"{start.replace('.', ':')}-{end.replace('.', ':')}" for start, end in times]
                
                if formatted_times:
                    final_data[q] = formatted_times
                else:
                    print(f"Очередь {q}: время не найдено в тексте")
                    final_data[q] = [] # Пусто, если сайт реально не дал график
            
        except Exception as e:
            print(f"Ошибка на очереди {q}: {e}")

    # Если совсем ничего не нашли, не перезаписываем файл пустышкой
    if final_data and any(final_data.values()):
        with open('schedules.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)
        print("Файл успешно обновлен!")
    else:
        print("Данные не получены, файл не изменен.")

if __name__ == "__main__":
    parse_soe()
