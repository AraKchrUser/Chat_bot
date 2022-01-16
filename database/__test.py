import psycopg2

conn = psycopg2.connect(dbname='postgres', user='arm', password='armkchr', host='localhost', port="5432")
cursor = conn.cursor()
# print(conn.get_dsn_parameters())
create_table_query = '''CREATE TABLE mobile
                          (ID INT PRIMARY KEY     NOT NULL,
                          MODEL           TEXT    NOT NULL,
                          PRICE         REAL); '''
cursor.execute(create_table_query)
conn.commit()
insert_query = """ INSERT INTO mobile (ID, MODEL, PRICE) VALUES (1, 'Iphone12', 1100)"""
cursor.execute(insert_query)
conn.commit()
print("1 запись успешно вставлена")
cursor.execute("SELECT * from mobile")
record = cursor.fetchall()
print("Результат", record)


