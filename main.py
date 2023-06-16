import requests
from fake_headers import Headers
import bs4
import json



headers = Headers(browser="firefox", os="win")
headers_data = headers.generate()

main_html = requests.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2", headers=headers_data).text
main_soup = bs4.BeautifulSoup(main_html, "lxml")

vacancy_list = main_soup.find_all("div", class_="serp-item")

all_vacancy = []

def get_vacancy_json():
    for vacancy in vacancy_list:
        div_city = vacancy.find(attrs={"data-qa":"vacancy-serp__vacancy-address"})
        div_name_vacancy = vacancy.find("a", class_="serp-item__title")
        div_salary = vacancy.find("span", class_="bloko-header-section-3")
        if div_salary == None:
            continue

        all_vacancy.append(
            {
            "vacancy":div_name_vacancy.text,
            "city":div_city.text.split(',')[0],
            "salary":div_salary.text.replace(" ", ""),
            "link":div_name_vacancy['href']
            }
        )




if __name__ == '__main__':
    get_vacancy_json()
    with open('vacancy_list_1.json', "w", encoding="utf8") as f:
        json.dump(all_vacancy, f, indent=4, ensure_ascii=False)
