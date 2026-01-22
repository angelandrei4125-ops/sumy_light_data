import requests
import json
import re

def parse_soe():
    # URL для получения данных
    api_url = 'https://www.soe.com.ua/spozhivacham/vidklyuchennya/get-gpv-data'
    
    queues = ["1.1", "1.2", "2.1", "2.2", "3.1", "3.2", "4.1", "4.2", "5.1", "5.2", "6.1", "6.2"]
    final_data = {}

    for q in queues:
        try:
            # Имитируем запрос от браузера
            response = requests.post(api_url, data={'queue': q}, timeout=15)
            
            if response.status_code == 200:
                html_content = response.text
                
                # Ищем все временные интервалы формата 00:00-04:00 или 00:00 - 04:00
                # Этот паттерн вытащит именно цифры
                times = re.findall(r'(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})', html_content)
                
                # Превращаем найденные пары в список строк "00:00-04:00"
                formatted_times = [f"{start}-{end}" for start, end in times]
                
                # Если сайт выдал пустой список, оставим старый график как запасной
                if formatted_times:
                    final_data[q] = formatted_times
                else:
                    print(f"Предупреждение: Для очереди {q} время не найдено в HTML")
                    # Запасной вариант, чтобы приложение не упало
                    final_data[q] = ["00:00-00:00"] 

            print(f"Очередь {q} успешно спарсена: {final_data.get(q)}")
            
        except Exception as e:
            print(f"Ошибка на очереди {q}: {e}")

    # Сохраняем реальные данные в JSON
    with open('schedules.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    parse_soe()
