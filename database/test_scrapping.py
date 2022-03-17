import bs4
import requests
import time
import pandas as pd
import logging


def get_data():
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
    # question, answer = get_data()
    # pd.DataFrame({'question': question, 'answer': answer}).to_csv('FAQ.csv')
    # url = "https://mfc-amur.ru/faq/693244/"
    # page = requests.get(url)
    # soup = bs4.BeautifulSoup(page.content, 'html.parser')
    # print(soup.find(class_="news-detail__detail-text").text)
    df = pd.read_csv('FAQ.csv')
    print(df.info())
    print(df.dropna())
