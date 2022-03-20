import pandas as pd
from database.entity import *
from database.db_session import *
import csv


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
