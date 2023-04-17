
import requests
import super_job
import statistics


def get_vacancies(vacancy='Python'):
    request_period = 30
    page = -1
    pages_number = 1
    vacancies = []
    while page < pages_number:
        page += 1
        url = 'https://api.hh.ru/vacancies'
        payload = {
            'text': vacancy,
            'city': 'Москва',
            'period': f'{request_period}',
            'page': page
        }
        response = requests.get(url, params=payload)
        response.raise_for_status()
        page_payload = response.json()
        pages_number = min(5, page_payload['pages'])
        vacancies.append(page_payload)
    return vacancies


def predict_rub_salary(vacancy):
    if vacancy['currency'] != 'RUR':
        return None
    salary_from = vacancy['from']
    if not salary_from:
        salary_from = None
    salary_to = vacancy['to']
    if not salary_to:
        salary_to = None
    return super_job.predict_salary(salary_from, salary_to)


def get_language_statistic(vacancy_name):
    vacancies_pages = get_vacancies(vacancy_name)
    salaries = []
    vacancies_found = 0
    for vacancies in vacancies_pages:
        for index, vacancy in enumerate(vacancies['items']):
            vacancies_found += 1
            if not vacancy['salary']:
                continue
            if vacancy['salary']['currency'] != 'RUR':
                continue
            salaries.append(predict_rub_salary(vacancy['salary']))
    if len(salaries):
        average_salary = int(statistics.mean(salaries))
    else:
        average_salary = 0
    language_stat = {
        'vacancies_found': vacancies_found,
        'vacancies_processed': len(salaries),
        'average_salary': average_salary
    }
    return language_stat


def get_statistic(languages):
    languages_statistic = {}
    for language in languages:
        languages_statistic[language] = get_language_statistic(language)
    return languages_statistic


def main():
    languages = [
        'python',
        'java',
        'javascript',
    ]
    get_statistic(languages)


if __name__ == '__main__':
    main()
