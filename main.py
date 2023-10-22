import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from fake_headers import Headers
import json
from pprint import pprint
import re
def get_info(vacancy):
   city = vacancy.find('div', attrs={"data-qa": "vacancy-serp__vacancy-address"}).text
   company = vacancy.find('a', attrs={"data-qa": "vacancy-serp__vacancy-employer"})
   company = company.text if company is not None else ''
   company = re.sub(r'\xa0', ' ', company)
   salary = vacancy.find('span', attrs={"data-qa": "vacancy-serp__vacancy-compensation"})
   salary = salary.text if salary is not None else ''
   salary = re.sub(r'\u202f',' ', salary)
   link = vacancy.find('a', attrs={"data-qa": "serp-item__title"})["href"]
   return {
       "city":city,
       "company": company,
       "salary": salary,
       "link": link
   }
def check(vacancy):
    page = requests.get(vacancy['link'],
                        headers=Headers(browser='chrome').generate())
    soup = BeautifulSoup(page.text, 'html.parser')
    description = soup.find('div', attrs={"data-qa": "vacancy-description"}).text
    return 'Django' in description or 'Flask' in description

if __name__ == "__main__":
    page = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2',
                        headers=Headers(browser ='chrome').generate())

    soup = BeautifulSoup(page.text, 'html.parser')
    vacancies = soup.find_all( 'div', class_="vacancy-serp-item-body")
    vacancies_info =[get_info(vacancy) for vacancy in vacancies]
   # pprint(vacancies_info)
    suitable_vacancies = [vacancy for vacancy in vacancies_info if check(vacancy)]
    pprint(suitable_vacancies)
    with open('data. json', 'w') as file:
        json.dump(suitable_vacancies, file, indent=4, ensure_ascii=False)
