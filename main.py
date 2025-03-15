import datetime
import requests
import csv
import time  

base_url = "https://api.hh.kz/vacancies"
headers = {
    "Authorization": "Bearer APPLTOF9GDHIK0OR2RC8FHTUI10OBDGC4P4UI2G59HG871T6TVEAJUD9QJ5H4S8S"  # Ваш токен
}

per_page = 100  
delay_seconds = 1  

def fetch_vacancies(date_from, date_to, city_id, page):
    """ Получить вакансии для конкретного интервала времени, города и страницы """
    params = {
        "area": city_id,
        "date_from": date_from,
        "date_to": date_to,
        "per_page": per_page,
        "page": page
    }
    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка при запросе для города {city_id} на странице {page}: {response.status_code}")
        return None

def collect_vacancies_for_today(cities_ids):
    """ Собрать вакансии для всех городов за сегодняшний день """
    today = datetime.datetime.today()
    date_from = today.strftime('%Y-%m-%dT00:00:00')
    date_to = today.strftime('%Y-%m-%dT23:59:59')

    all_vacancies = []
    for city_id in cities_ids:
        page = 0
        while True:
            data = fetch_vacancies(date_from, date_to, city_id, page)
            if data and data.get('items'):
                all_vacancies.extend(data['items'])
                if len(data['items']) < per_page:
                    break
                page += 1
            else:
                break
            time.sleep(delay_seconds)  
    return all_vacancies

def parse_and_save_vacancies():
    today_str = datetime.datetime.today().strftime('%Y-%m-%d')
    print(f"Сбор вакансий за {today_str}")
    cities_ids = [
        6251, 6782, 11071, 11083, 2728, 150, 6254, 151, 152, 154, 6365, 156, 160, 169,
        158, 161, 11484, 6300, 6251, 6493, 159, 6529, 6511, 6510, 6351, 3663, 153, 5053,
        157, 2226, 11293, 6497, 164, 5118, 162, 6488, 163, 5055, 11180, 6778, 5129, 6431,
        6483, 11076, 11329, 165, 6287, 6292, 6343, 5124, 6347, 6446, 2510, 167, 6482, 6481,
        6496, 6104, 166, 11524, 6989, 6947, 6525, 2952, 11331, 11330, 6322, 6346, 6479, 168,
        11183, 11332, 6460, 175, 11237, 6509, 11163, 3074, 5054, 6358, 11072, 177, 6471, 178,
        6478, 11078, 11258, 6342, 2653, 5052, 6495, 173, 6513, 176, 171, 4491, 172, 6393, 6487,
        3034, 5051, 11162, 6780, 174, 180, 6395, 11275, 183, 182, 6501, 6502, 6476, 5126, 6017,
        4304, 2951, 6484, 6779, 6459, 184, 11073, 185, 6060, 2437, 5164, 6475, 5042, 3048, 188,
        6325, 187, 6474, 7003, 189, 190, 11194, 191, 6344, 6366, 192, 6248, 6935, 193, 6453, 194,
        6349, 6250, 6781, 195, 6473, 3704, 4637, 6348, 11231, 6388, 6500, 6290, 6499, 6108, 196, 6524,
        6324, 6498, 2729, 205, 197, 6948
    ]

    vacancies = collect_vacancies_for_today(cities_ids)

    print(f"Общее количество собранных вакансий: {len(vacancies)}")

    if vacancies:
        filename = f'vacancies_{today_str}.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'salary_from', 'salary_to', 'salary_currency', 'area', 'city', 'latitude', 'longitude', 
                             'professional_role', 'employment_type', 'requirement', 'responsibility', 'snippet', 
                             'employer_name', 'experience', 'published_at'])
            
            for vacancy in vacancies:
                id = vacancy.get('id')
                name = vacancy.get('name')
                salary = vacancy.get('salary')
                salary_from = salary['from'] if salary and 'from' in salary else None
                salary_to = salary['to'] if salary and 'to' in salary else None
                salary_currency = salary['currency'] if salary and 'currency' in salary else None
                area = vacancy.get('area', {}).get('name', None)
                city = area  
                
                address = vacancy.get('address')
                latitude = address.get('lat') if address else None
                longitude = address.get('lng') if address else None
                
                professional_roles = vacancy.get('professional_roles', [])
                professional_role = professional_roles[0].get('name') if professional_roles else None
                
                employment_type = vacancy.get('employment', {}).get('name', None)
                
                snippet_data = vacancy.get('snippet', {})
                requirement = snippet_data.get('requirement', 'Не указаны')
                responsibility = snippet_data.get('responsibility', 'Не указаны')
                snippet = f"{requirement} {responsibility}"
                
                employer_name = vacancy.get('employer', {}).get('name', 'Не указано')
                experience = vacancy.get('experience', {}).get('name', 'Не указано')
                published_at = vacancy.get('published_at', 'Не указано')
                
                writer.writerow([id, name, salary_from, salary_to, salary_currency, area, city, latitude, longitude, 
                                 professional_role, employment_type, requirement, responsibility, snippet, 
                                 employer_name, experience, published_at])
        
        print(f"Данные сохранены в файл '{filename}'.")
    else:
        print("Нет данных для записи в файл.")
    
parse_and_save_vacancies()
