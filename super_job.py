
import os
import requests
import pprint
import statistics


from dotenv import load_dotenv


def predict_rub_salary(vacancy):
    if vacancy['currency'] != 'rub':
        return None
    salary_from = vacancy['payment_from']
    if salary_from == 0:
        salary_from = None
    salary_to = vacancy['payment_to']
    if salary_to == 0:
        salary_to = None
    return predict_salary(salary_from, salary_to)


def predict_salary(salary_from, salary_to):
    if not salary_from and not salary_to:
        return None
    if not salary_to:
        return salary_from * 1.2
    elif not salary_from:
        return salary_to * 0.8
    else:
        return statistics.mean([salary_from, salary_to])


def get_vacancies(token, language, catalogues=33, count_per_page=100, town=14, page=1):
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


def get_statistic(token, languages, catalogues=33, town=14):
    languages_statistic = {}
    count_per_page = 100
    for language in languages:
        vacancies = []
        vacancies_salaries = []
        page, page_numbers = -1, 1
        while page <= page_numbers:
            page += 1
            vacancies_page = get_vacancies(token, language, catalogues, count_per_page, town, page)
            page_numbers = (vacancies_page['total'] // count_per_page) + 1
            for vacancy in vacancies_page['objects']:
                vacancies.append(vacancy)
                vacancy_salary = predict_rub_salary(vacancy)
                if vacancy_salary:
                    vacancies_salaries.append(vacancy_salary)
        if len(vacancies_salaries):
            average_salary = int(statistics.mean(vacancies_salaries))
        else:
            average_salary = 0
        languages_statistic[language] = {
            'vacancies_found': len(vacancies),
            'vacancies_processed': len(vacancies_salaries),
            'average_salary': average_salary
        }
    return languages_statistic


def main():
    load_dotenv()
    token = os.environ['SJ_TOKEN']
    languages = [
        'python',
        'java',
        'javascript',
    ]
    stat = get_statistic(token, languages)
    pprint.pprint(stat)


if __name__ == '__main__':
    main()
