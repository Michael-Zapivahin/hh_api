

import head_hunter



from dotenv import load_dotenv


def main():
    vacancies = head_hunter.load_vacancies()
    for vacancy in vacancies['items']:
        print(vacancy['salary'])




if __name__ == '__main__':
    main()


