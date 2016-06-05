import psycopg2
import sys
import os
import json
import time
import psycopg2.extras
import kafka
import decimal

from kafka import KafkaConsumer

#connection
conn_string = "dbname='salesbi' user='salesbi'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

#get data from the database into a list
cur.execute("""SELECT sales_rep_id,sales_rep_territory,daily_gallon_plan from sales_rep""")
sales_rows = cur.fetchall()
cur.execute("""SELECT product_id,gallons from product""")
prod_rows = cur.fetchall()
cur.execute("""SELECT territory_id,territory_name from territory""")
terr_rows = cur.fetchall()
cur.close()
conn.close()

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
sales = {}
sales['NE']={}
sales['SE']={}
sales['NYC']={}
sales['GL']={}
sales['WC']={}
sales['TX']={}

#compute for plan per territory
for row in sales_rows:
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

sales['NE']['Name'] = "North East"
sales['NE']['Plan'] = NE_plan
sales['NE']['Act']=0.0
sales['NE']['Ave']=0.0
sales['NE']['Stat']=0

sales['SE']['Name'] = "South East"
sales['SE']['Plan'] = SE_plan
sales['SE']['Act']=0.0
sales['SE']['Ave']=0.0
sales['SE']['Stat']=0

sales['NYC']['Name'] = "New York Metro"
sales['NYC']['Plan'] = NYC_plan
sales['NYC']['Act']=0.0
sales['NYC']['Ave']=0.0
sales['NYC']['Stat']=0

sales['GL']['Name'] = "Great Lakes"
sales['GL']['Plan'] = GL_plan
sales['GL']['Act']=0.0
sales['GL']['Ave']=0.0
sales['GL']['Stat']=0

sales['WC']['Name'] = "West Coast"
sales['WC']['Plan'] = WC_plan
sales['WC']['Act']=0.0
sales['WC']['Ave']=0.0
sales['WC']['Stat']=0

sales['TX']['Name'] = "Texas"
sales['TX']['Plan'] = TX_plan
sales['TX']['Act']=0.0
sales['TX']['Ave']=0.0
sales['TX']['Stat']=0


#read message from kafka
consumer = KafkaConsumer('transaction_slot')
print('consumer created')

for message in consumer:
    print '==='
    print len(sales), ':', json.dumps(sales)
    if len(message) == 0:
      continue
    event1 = json.loads(message.value)
    prod_id = event1['product_id'].encode('ascii', 'ignore')
    units= event1['unit_sold'].encode('ascii', 'ignore')
    sales_rep = event1['sales_rep_id'].encode('ascii', 'ignore')
    tstamp = event1['timestamp'].encode('ascii','ignore')
    for row in sales_rows:
       if row[0]==sales_rep:
          terr=row[1]
    for row in prod_rows:
       if row[0]==prod_id:
         gallons = float(row[1])
         gallon_sales = float(units)*gallons
         
    if terr == 'WC':
        sales['WC']['tstamp'] = tstamp
        sales_ave = (gallon_sales - sales['WC']['Act']) / 2
        if sales_ave < sales['WC']['Ave']:
            sales['WC']['Stat'] = -1
        elif sales_ave == sales['WC']['Ave']:
            sales['WC']['Stat'] = 0
        else:
            sales['WC']['Stat'] = 1
        sales['WC']['Ave'] = str(sales_ave)
        sales['WC']['Act'] = sales['WC']['Act'] + gallon_sales
    elif terr=='NE':
	sales['NE']['tstamp'] = tstamp
        sales_ave = (gallon_sales - sales['NE']['Act'])/2
        if sales_ave < sales['NE']['Ave']:
            sales['NE']['Stat']= -1
        elif sales_ave == sales['NE']['Ave']:
            sales['NE']['Stat']=0
        else:
            sales['NE']['Stat']= 1
        sales['NE']['Ave'] = str(sales_ave)
        sales['NE']['Act']= sales['NE']['Act'] + gallon_sales
    elif terr == 'SE':
        sales['SE']['Tstamp'] = tstamp
        sales_ave = (gallon_sales - sales['SE']['Act']) / 2
        if sales_ave < sales['SE']['Ave']:
            sales['SE']['Stat'] = -1
        elif sales_ave == sales['SE']['Ave']:
            sales['SE']['Stat'] = 0
        else:
            sales['SE']['Stat'] = 1
        sales['SE']['Ave'] = str(sales_ave)
        sales['SE']['Act'] = sales['SE']['Act'] + gallon_sales
    elif terr == 'NYC':
        sales['NYC']['Tstamp'] = tstamp
        sales_ave = (gallon_sales - sales['NYC']['Act']) / 2
        if sales_ave < sales['NYC']['Ave']:
            sales['NYC']['Stat'] = -1
        elif sales_ave == sales['NYC']['Ave']:
            sales['NYC']['Stat'] = 0
        else:
            sales['NYC']['Stat'] = 1
        sales['NYC']['Ave'] = str(sales_ave)
        sales['NYC']['Act'] = sales['NYC']['Act'] + gallon_sales
    elif terr == 'GL':
        sales['GL']['Tstamp'] = tstamp
        sales_ave = (gallon_sales - sales['GL']['Act']) / 2
        if sales_ave < sales['GL']['Ave']:
            sales['GL']['Stat'] = -1
        elif sales_ave == sales['GL']['Ave']:
            sales['GL']['Stat'] = 0
        else:
            sales['GL']['Stat'] = 1
        sales['GL']['Ave'] = str(sales_ave)
        sales['GL']['Act'] = sales['GL']['Act'] + gallon_sales
    elif terr == 'TX':    
        sales['TX']['tstamp'] = tstamp
        sales_ave = (gallon_sales - sales['TX']['Act']) / 2
        if sales_ave < sales['TX']['Ave']:
            sales['TX']['Stat'] = -1
        elif sales_ave == sales['TX']['Ave']:
            sales['TX']['Stat'] = 0
        else:
            sales['TX']['Stat'] = 1
        sales['TX']['Ave'] = str(sales_ave)
        sales['TX']['Act'] = sales['TX']['Act'] + gallon_sales
