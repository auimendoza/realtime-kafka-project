import psycopg2
import sys
import os
import json
import time
import kafka
import decimal

from kafka import KafkaConsumer

class SalesConsumer():

  def __init__(self, topic):
    #connection
    self.topic = topic
    conn_string = "dbname='salesbi' user='salesbi'"
    self.conn = psycopg2.connect(conn_string)
    self.cur = self.conn.cursor()
    self.sales = {}
    self.reps = {}
    self.prods = {}
    
  def getrefs(self):
    #get data from the database into a list
    self.cur.execute("""SELECT sales_rep_id,sales_rep_territory,daily_gallon_plan from sales_rep""")
    self.sales_rows = self.cur.fetchall()

    for sr in self.sales_rows:
      self.reps[sr[0]] = {'TerritoryId':sr[1], 'Plan':sr[2]}

    self.cur.execute("""SELECT product_id,gallons from product""")
    self.prod_rows = self.cur.fetchall()

    for p in self.prod_rows:
      self.prods[p[0]] = {'Gallons': p[1]}

    self.cur.execute(
      """
      SELECT territory_id,territory_name, SUM(daily_gallon_plan) plan 
        from territory t, sales_rep r
       WHERE r.sales_rep_territory = t.territory_id
       GROUP BY t.territory_id, t.territory_name
      """
    )
    self.terr_rows = self.cur.fetchall()
   
    for t in self.terr_rows:
      self.sales[t[0]] = {'Name':t[1], 'Plan':t[2], 'Act':0.0, 'Ave':0.0, 'Stat':0, 'Tstamp':''}
    
    self.cur.close()
    self.conn.close()

  def getconsumer(self):
    #read message from kafka
    self.consumer = KafkaConsumer(self.topic)
    print self.topic, 'consumer created'
    return self.consumer
    
  def getsales(self, message):
    #print len(self.sales)
    event1 = json.loads(message.value)
    prod_id = event1['product_id'].encode('ascii', 'ignore')
    units= event1['unit_sold'].encode('ascii', 'ignore')
    sales_rep = event1['sales_rep_id'].encode('ascii', 'ignore')
    tstamp = event1['timestamp'].encode('ascii','ignore')

    territory = self.reps[sales_rep]['TerritoryId']
    gallons = float(self.prods[prod_id]['Gallons'])*float(units)

    self.sales[territory]['Tstamp'] = tstamp

    actual = self.sales[territory]['Act'] + gallons
    self.sales[territory]['Act'] = actual

    ave = (self.sales[territory]['Ave'] + gallons)/2
    self.sales[territory]['Ave'] = ave
   
    plan = float(self.sales[territory]['Plan'])
   
    if actual > plan:
      self.sales[territory]['Stat'] = 1
    elif actual == plan:
      self.sales[territory]['Stat'] = 0
    elif actual < plan:
      self.sales[territory]['Stat'] = -1
        

if __name__ == '__main__':
  sc = SalesConsumer('transaction_slot')
  sc.getrefs()
  for msg in sc.getconsumer():
    if len(msg.value) == 0:
      continue
    sc.getsales(msg)
    print json.dumps(sc.sales)
  
