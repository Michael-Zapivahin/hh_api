

import head_hunter
import super_job
import os

from terminaltables import AsciiTable

from dotenv import load_dotenv
def print_table(title, data):
    table_data = []
    table_data.append(['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'])
    for index, language in enumerate(data):
        table_data.append(
            [
                language,
                data[language]['vacancies_found'],
                data[language]['vacancies_processed'],
                data[language]['average_salary'],
            ]
        )
    table = AsciiTable(table_data, title)
    print(table.table)



def main():
    load_dotenv()
    token = os.environ['SJ_TOKEN']
    languages = [
        'python',
        'java',
        'javascript',
    ]
    print_table('SuperJob Moscow', super_job.get_statistic(token, languages))
    print_table('Head hunter Moscow', head_hunter.get_statistic(languages))



if __name__ == '__main__':
    main()


