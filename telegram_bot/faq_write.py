import pandas as pd
from database.entity import *
from database.db_session import *
import csv
from database.test_scrapping import get_service_description_mfc


def faq_write():
    db_sess = create_session()
    file_name = 'faqdumps.csv'
    outfile = open(file_name, 'w')
    outcsv = csv.writer(outfile,  csv.QUOTE_MINIMAL)
    records = db_sess.query(FAQ).all()
    [outcsv.writerow([getattr(curr, column.name) for column in FAQ.__mapper__.columns]) for curr in records]
    outfile.close()
    df = pd.read_csv(file_name, sep=',', header=None, names=['Question', 'Answer'])
    df.to_csv(file_name, index=False)
    return file_name


def service_write(file_flag=True):
    db_sess = create_session()
    file_name = 'services_with_description.csv'
    outfile = open(file_name, 'w')
    outcsv = csv.writer(outfile, csv.QUOTE_MINIMAL)
    records = db_sess.query(Service).all()
    [outcsv.writerow([getattr(curr, column.name) for column in Service.__mapper__.columns]) for curr in records]
    outfile.close()
    df = pd.read_csv(file_name, sep=',', header=None, names=['Question', 'Answer'])
    answer = df.Answer + '[sep]' + df.Question
    df = pd.concat([df['Question'], answer], axis=1)
    df.columns = ['Question', 'Answer']
    df.to_csv(file_name, index=False)
    df = pd.read_csv(file_name, sep=',')

    serv_desc = get_service_description_mfc()
    services = []
    for i in serv_desc:
        services.append(i[0])
    question = pd.Series(services) + ' ' + df.Question
    df = pd.concat([question, df['Answer']], axis=1)
    df.columns = ['Question', 'Answer']

    df.to_csv(file_name, index=False)
    return file_name


if __name__ == "__main__":
    global_init("postgre1")
    service_write(file_flag=False)
