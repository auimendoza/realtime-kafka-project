
import psycopg2
import time
try:
#    conn = psycopg2.connect("dbname=salesdb user=postgres password=postgres")
    conn = psycopg2.connect("dbname=salesbi user=salesbi")
except:
    print "I am unable to connect to the database"

cur = conn.cursor()

for i in range (0,100):
    cur.execute("""SELECT create_transaction()""")
    cur.execute("""SELECT count(*) from transaction""")
    time.sleep(5)
    rows = cur.fetchall()
    for row in rows:
        print "no of transactions created ", row[0]
        conn.commit()



