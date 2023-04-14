
import requests
import super_job
import statistics

def load_vacancies(vacancy='Python'):
    page = -1
    pages_number = 1
    result = []
    while page < pages_number:
        page += 1
        url = 'https://api.hh.ru/vacancies'
        payload = {
            'text': vacancy,
            'city': 'Москва',
            'period': '30',
            'page': page
        }
        response = requests.get(url, params=payload)
        response.raise_for_status()
        page_payload = response.json()
        pages_number = min(5, page_payload['pages'])
        result.append(page_payload)
    return result


def predict_rub_salary(vacancy):
    if vacancy['currency'] == 'RUR':
        salary_from = vacancy['from']
        if salary_from == 0:
            salary_from = None
        salary_to = vacancy['to']
        if salary_to == 0:
            salary_to = None
        return super_job.predict_salary(salary_from, salary_to)
    else:
        return None


def get_salaries(vacancy_name):
    vacancies_pages = load_vacancies(vacancy_name)
    salaries = []
    vacancies_found = 0
    for vacancies in vacancies_pages:
        for index, vacancy in enumerate(vacancies['items']):
            vacancies_found += 1
            if vacancy['salary'] is None:
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
    language_stat = {}
    for language in languages:
        language_stat[language] = get_salaries(language)
    return language_stat


def main():
    languages = [
        'python',
        'java',
        'javascript',
    ]
    get_statistic(languages)


if __name__ == '__main__':
    main()
