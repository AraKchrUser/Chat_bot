import bs4
import requests
import time
import pandas as pd
import logging
from pprint import pprint


def get_sirvices():
    target = []
    service = []
    refs = []
    url = "https://mfc-spravka.ru/uslugi-mfc.html"
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    service_list = [[tag.get_text() for tag in child.find_all('a')] for child in soup.find_all("tbody")]
    dict_data = {
        "Жилищные услуги": service_list[0],
        "Справки и выписки": service_list[2],
        "Семья и дети": service_list[3],
        "Социальные услуги": service_list[4],
        "Транспорт и вождение": service_list[5],
        "Здоровье": service_list[6],
        "Прописка и гражданство": service_list[7],
        "Паспорт РФ и загранпаспорт": service_list[8],
        "ИНН и СНИЛС": service_list[9],
        "Разрешения и лицензии": service_list[10],
        "Налоги и бизнес": service_list[11]
    }

    url = "https://mfc-spravka.ru/uslugi-mfc.html"
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    ref = [[tag['href'] for tag in child.find_all('a')] for child in soup.find_all("tbody")]

    for k, v, in dict_data.items():
        target.extend([k] * len(v))
        service.extend(v)

    for i in [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
        refs.extend(ref[i])

    return target, target, service, refs


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


def get_news():
    url = "https://mfc-amur.ru/news/"
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    struct = {}
    for count, item in enumerate(soup.find_all(class_='news__item row')[::-1][:5]):
        key_date = item.find(class_='news__item-date col-xs-12').text
        href = item.find(class_='news-link')['href']
        news_ = bs4.BeautifulSoup(requests.get('https://mfc-amur.ru' + href).content,
                                  'html.parser').find(class_='news-detail__detail-text')
        news_text = ''
        if news_:
            news_text = ' '.join([elem.text for elem in news_])
        struct[key_date + '|' + str(count)] = ('https://mfc-amur.ru' + href, ' '.join(news_text.split()))

    return struct


def get_service_description_mfc():
    texts = []
    items = get_sirvices()
    refs = items[-1]
    for ref in refs:
        page = requests.get(ref)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        texts.append([' '.join([' '.join(tag.text.split()) for tag in soup.find(id='main').find_all('p')])])

    return texts


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
    # for i, r in zip(*get_sirvices()):
    #     print(i, r)
    # target, target, service, refs = get_sirvices()
    # print(len(refs))
    # pd.DataFrame({'question': target, 'answer0': target, 'answer1': service, 'docs': refs}).to_csv('QAService.csv')
    # Записать в файл в 3 колонки для faq
    # url = "https://mfc-spravka.ru/uslugi-mfc.html"
    # page = requests.get(url)
    # soup = bs4.BeautifulSoup(page.content, 'html.parser')
    # pprint([[tag.get_text() for tag in child.find_all('a')] for child in soup.find_all("tbody")])
    # url = "https://mfc-spravka.ru/uslugi-mfc.html"
    # page = requests.get(url)
    # soup = bs4.BeautifulSoup(page.content, 'html.parser')
    # pprint([[tag['href'] for tag in child.find_all('a')] for child in soup.find_all("tbody")])
    # pprint(get_news())
    print(get_service_description_mfc())
