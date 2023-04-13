
import os
import vacancies
import pprint



from dotenv import load_dotenv


def main():
    vacan = vacancies.load_vacancies()
    for v in vacan['items']:
        print(v['salary'])




if __name__ == '__main__':
    main()


