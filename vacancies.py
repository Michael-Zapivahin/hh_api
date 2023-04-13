
import requests


def load_vacancies(vacancy='Python'):
    page = 0
    pages_number = 1
    result = []
    while page < pages_number:
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
        pages_number = page_payload['pages']
        page += 1
        result.append(page_payload)
    return result


def predict_rub_salary(vacancy_name):
    vacancies_pages = load_vacancies()
    result = []
    for vacancies in vacancies_pages:
        for index, vacancy in enumerate(vacancies['items']):
            if vacancy['salary'] is None:
                continue
            if vacancy['salary']['currency'] !='RUR':
                # result.append(None)
                continue
            if vacancy['salary']['from'] is None:
                result.append(int(vacancy['salary']['to'])*0.8)
            elif vacancy['salary']['to'] is None:
                result.append(int(vacancy['salary']['from']) * 1.2)
            else:
                result.append((int(vacancy['salary']['from'])+int(vacancy['salary']['to']))/2)
    return result

def main():
    cost = predict_rub_salary('Python')
    print(int(sum(cost)/len(cost)))


if __name__ == '__main__':
    main()