
import head_hunter
import super_job
import os


from terminaltables import AsciiTable
from dotenv import load_dotenv


def print_statistic(title, statistic):
    statistic_salaries = []
    statistic_salaries.append(['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'])
    for index, language in enumerate(statistic):
        statistic_salaries.append(
            [
                language,
                statistic[language]['vacancies_found'],
                statistic[language]['vacancies_processed'],
                statistic[language]['average_salary'],
            ]
        )
    table = AsciiTable(statistic_salaries, title)
    print(table.table)


def main():
    load_dotenv()
    token = os.environ['SJ_TOKEN']
    languages = [
        'python',
        'java',
        'javascript',
    ]
    print_statistic('SuperJob Moscow', super_job.get_statistic(token, languages))
    print_statistic('Head hunter Moscow', head_hunter.get_statistic(languages))


if __name__ == '__main__':
    main()
