import psycopg2
import sys
import os
import json
import time
import psycopg2.extras
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
    self.sales= {}
    
  def getrefs(self):
    #get data from the database into a list
    self.cur.execute("""SELECT sales_rep_id,sales_rep_territory,daily_gallon_plan from sales_rep""")
    self.sales_rows = self.cur.fetchall()
    self.cur.execute("""SELECT product_id,gallons from product""")
    self.prod_rows = self.cur.fetchall()
    self.cur.execute("""SELECT territory_id,territory_name from territory""")
    self.terr_rows = self.cur.fetchall()
    self.cur.close()
    self.conn.close()
    
    gallon_sales=0
    gallon_plan=0
    ind_stat = 0
    terr_sales = 0
    gallons=0
    
    #initialize all gallon plans
    NE_plan = 0
    SE_plan=0
    NYC_plan = 0
    GL_plan=0
    WC_plan=0
    TX_plan=0
    
    #inititalize all status
    NE_stat = 0
    SE_stat = 0
    NYC_stat = 0
    GL_stat = 0
    WC_stat = 0
    TX_stat=0
    
    terr=''
    terr_name=''
    
    #initialize the dictionary of final results
    self.sales['NE']={}
    self.sales['SE']={}
    self.sales['NYC']={}
    self.sales['GL']={}
    self.sales['WC']={}
    self.sales['TX']={}
    
    #compute for plan per territory
    for row in self.sales_rows:
        if row[1]== "NE":
            NE_plan = NE_plan + row[2]
        elif row[1] == "SE":
            SE_plan = SE_plan + row[2]
        elif row[1] == "NYC":
            NYC_plan = NYC_plan + row[2]
        elif row[1] == "GL":
            GL_plan = GL_plan + row[2]
        elif row[1] == "WC":
            WC_plan = WC_plan + row[2]
        elif row[1] == "TX":    
            TX_plan = TX_plan + row[2]
    
    self.sales['NE']['Name'] = "North East"
    self.sales['NE']['Plan'] = NE_plan
    self.sales['NE']['Act']=0.0
    self.sales['NE']['Ave']=0.0
    self.sales['NE']['Stat']=0
    
    self.sales['SE']['Name'] = "South East"
    self.sales['SE']['Plan'] = SE_plan
    self.sales['SE']['Act']=0.0
    self.sales['SE']['Ave']=0.0
    self.sales['SE']['Stat']=0
    
    self.sales['NYC']['Name'] = "New York Metro"
    self.sales['NYC']['Plan'] = NYC_plan
    self.sales['NYC']['Act']=0.0
    self.sales['NYC']['Ave']=0.0
    self.sales['NYC']['Stat']=0
    
    self.sales['GL']['Name'] = "Great Lakes"
    self.sales['GL']['Plan'] = GL_plan
    self.sales['GL']['Act']=0.0
    self.sales['GL']['Ave']=0.0
    self.sales['GL']['Stat']=0
    
    self.sales['WC']['Name'] = "West Coast"
    self.sales['WC']['Plan'] = WC_plan
    self.sales['WC']['Act']=0.0
    self.sales['WC']['Ave']=0.0
    self.sales['WC']['Stat']=0
    
    self.sales['TX']['Name'] = "Texas"
    self.sales['TX']['Plan'] = TX_plan
    self.sales['TX']['Act']=0.0
    self.sales['TX']['Ave']=0.0
    self.sales['TX']['Stat']=0
    
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
    for row in self.sales_rows:
       if row[0]==sales_rep:
          terr=row[1]
    for row in self.prod_rows:
       if row[0]==prod_id:
         gallons = float(row[1])
         gallon_sales = float(units)*gallons
         
    if terr == 'WC':
       self.sales['WC']['tstamp'] = tstamp
       sales_ave = (gallon_sales -self.sales['WC']['Act']) / 2
       if sales_ave <self.sales['WC']['Ave']:
          self.sales['WC']['Stat'] = -1
       elif sales_ave ==self.sales['WC']['Ave']:
          self.sales['WC']['Stat'] = 0
       else:
          self.sales['WC']['Stat'] = 1
       self.sales['WC']['Ave'] = str(sales_ave)
       self.sales['WC']['Act'] = self.sales['WC']['Act'] + gallon_sales
    elif terr=='NE':
       self.sales['NE']['tstamp'] = tstamp
       sales_ave = (gallon_sales -self.sales['NE']['Act'])/2
       if sales_ave <self.sales['NE']['Ave']:
          self.sales['NE']['Stat']= -1
       elif sales_ave ==self.sales['NE']['Ave']:
          self.sales['NE']['Stat']=0
       else:
          self.sales['NE']['Stat']= 1
       self.sales['NE']['Ave'] = str(sales_ave)
       self.sales['NE']['Act']= self.sales['NE']['Act'] + gallon_sales
    elif terr == 'SE':
       self.sales['SE']['Tstamp'] = tstamp
       sales_ave = (gallon_sales -self.sales['SE']['Act']) / 2
       if sales_ave <self.sales['SE']['Ave']:
          self.sales['SE']['Stat'] = -1
       elif sales_ave ==self.sales['SE']['Ave']:
          self.sales['SE']['Stat'] = 0
       else:
          self.sales['SE']['Stat'] = 1
       self.sales['SE']['Ave'] = str(sales_ave)
       self.sales['SE']['Act'] = self.sales['SE']['Act'] + gallon_sales
    elif terr == 'NYC':
       self.sales['NYC']['Tstamp'] = tstamp
       sales_ave = (gallon_sales -self.sales['NYC']['Act']) / 2
       if sales_ave <self.sales['NYC']['Ave']:
          self.sales['NYC']['Stat'] = -1
       elif sales_ave ==self.sales['NYC']['Ave']:
          self.sales['NYC']['Stat'] = 0
       else:
          self.sales['NYC']['Stat'] = 1
       self.sales['NYC']['Ave'] = str(sales_ave)
       self.sales['NYC']['Act'] = self.sales['NYC']['Act'] + gallon_sales
    elif terr == 'GL':
       self.sales['GL']['Tstamp'] = tstamp
       sales_ave = (gallon_sales -self.sales['GL']['Act']) / 2
       if sales_ave <self.sales['GL']['Ave']:
          self.sales['GL']['Stat'] = -1
       elif sales_ave ==self.sales['GL']['Ave']:
          self.sales['GL']['Stat'] = 0
       else:
          self.sales['GL']['Stat'] = 1
       self.sales['GL']['Ave'] = str(sales_ave)
       self.sales['GL']['Act'] = self.sales['GL']['Act'] + gallon_sales
    elif terr == 'TX':    
       self.sales['TX']['tstamp'] = tstamp
       sales_ave = (gallon_sales -self.sales['TX']['Act']) / 2
       if sales_ave <self.sales['TX']['Ave']:
          self.sales['TX']['Stat'] = -1
       elif sales_ave ==self.sales['TX']['Ave']:
          self.sales['TX']['Stat'] = 0
       else:
          self.sales['TX']['Stat'] = 1
       self.sales['TX']['Ave'] = str(sales_ave)
       self.sales['TX']['Act'] = self.sales['TX']['Act'] + gallon_sales

if __name__ == '__main__':
  sc = SalesConsumer('transaction_slot')
  sc.getrefs()
  for msg in sc.getconsumer():
    if len(msg.value) == 0:
      continue
    sc.getsales(msg)
    print json.dumps(sc.sales)
  
