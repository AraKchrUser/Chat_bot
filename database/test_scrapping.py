import bs4
import requests
import time
import pandas as pd
import logging
from pprint import pprint


def get_sirvices():
    target = []
    service = []
    dict_data = {
        "Жилищные услуги": [1, 2, 3],
        "Социальные услуги": [1, 2, 3],
        "Справки и выписки": [1, 2, 3],
        "Семья и дети": [1, 2, 3],
        "Транспорт и вождение": [1, 2, 3],
        "Здоровье": [1, 2, 3],
        "Прописка и гражданство": [1, 2, 3],
        "Паспорт РФ и загранпаспорт": [1, 2, 3],
        "ИНН и СНИЛС": [1, 2, 3],
        "Налоги и бизнес": [1, 2, 3],
        "Разрешения и лицензии": [1, 2, 3]
    }
    for k, v in dict_data.items():
        target.extend([k] * len(v))
        service.extend(v)
    return target, service


def get_data_faq():
    url = "https://mfc-amur.ru/faq/?PAGEN_1="
    page_id = 1
    question = []
    answer = []
    while page_id < 125:
        page = requests.get(url + str(page_id))
        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        for faq in [item['href'] for item in soup.find_all(class_='readmore')][1:]:
            try:
                faq_url = "https://mfc-amur.ru" + faq
                data = bs4.BeautifulSoup(requests.get(faq_url).content, 'html.parser')
                qu = data.find(class_="news-detail").h2.text
                ans = data.find(class_="news-detail__detail-text").text
                if qu and ans:
                    question.append(qu)
                    answer.append(ans)
                time.sleep(0.1)
                logging.warning(faq)
            except:
                continue
        logging.warning(page_id)
        page_id += 1
    return question, answer


if __name__ == "__main__":
    # question, answer = get_data_faq()
    # pd.DataFrame({'question': question, 'answer': answer}).to_csv('FAQ.csv')
    # url = "https://mfc-amur.ru/faq/693244/"
    # page = requests.get(url)
    # soup = bs4.BeautifulSoup(page.content, 'html.parser')
    # print(soup.find(class_="news-detail__detail-text").text)
    # df = pd.read_csv('FAQ.csv')
    # print(df.info())
    # print(df.dropna())
    # for i, j in zip(*get_sirvices()):
    #     print(i, j)
    url = "https://mfc-spravka.ru/uslugi-mfc.html"
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    pprint([[tag.get_text() for tag in child.find_all('a')] for child in soup.find_all("tbody")])
    pprint(soup.find(id="content"))
    pass


