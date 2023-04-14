
import os
import requests
import pprint
import statistics
import itertools

from dotenv import load_dotenv

def predict_rub_salary_sj(vacancy):
    if vacancy['currency'] == 'rub':
        salary_from = vacancy['payment_from']
        if salary_from == 0:
            salary_from = None
        salary_to = vacancy['payment_to']
        if salary_to == 0:
            salary_to = None
        return predict_salary(salary_from, salary_to)
    else:
        return None

def predict_salary(salary_from, salary_to):
    if not salary_from and not salary_to:
        return None
    if not salary_to:
        return salary_from * 1.2
    elif not salary_from:
        return salary_to * 0.8
    else:
        return statistics.mean([salary_from, salary_to])

def get_vacancies(token, language, catalogues=33, count_per_page=100, town=14, page = 1):
    host = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': token,
        'Authorization': f'Bearer r.000000000000001.{token}'
    }
    payload = {
        'keyword': f'Программист {language}',
        'catalogues': catalogues,
        'page': page,
        'town': town,
        'count': count_per_page
    }
    response = requests.get(host, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()

def get_statiscics(token, languages, catalogues=33, town=14):
    language_statisic = {}
    count_per_page = 100
    for language in languages:
        vacancies = []
        for page in itertools.count(0):
            vacancies_page = get_vacancies(token, language, catalogues, count_per_page, town, page)
            pages = (vacancies_page['total'] // count_per_page) + 1
            if page >= pages:
                break
            for vacancy in vacancies_page['objects']:
                vacancies.append(vacancy)
                all_language_salaryes = [predict_rub_salary_sj(vacancy)]
            if len(all_language_salaryes) > 0:
                average_salary = statistics.mean(all_language_salaryes)
            else:
                average_salary = 0
            average_salary = int(average_salary)
            language_data = {
                'vacancies_found': vacancies_page['total'],
                'vacancies_processed': len(all_language_salaryes),
                'average_salary': average_salary
            }
            language_statisic[language] = language_data
    return language_statisic



def main():
    load_dotenv()
    token = os.environ['SJ_TOKEN']
    languages = [
        'python',
        'java',
        'javascript',
    ]
    stat = get_statiscics(token, languages)
    pprint.pprint(stat)


if __name__ == '__main__':
    main()
