import json
import psycopg2
import re, sys, time, traceback
from datetime import datetime
from kafka import KafkaProducer

con = None
cur = None

def startreplication (slot):
  # create slot
  plugin = 'test_decoding'
  cur.execute(
    '''
    SELECT pg_create_logical_replication_slot(%s, %s)
    '''
    , (slot, plugin))
  print slot, 'created.'

def getlogs():
  draw = []
  d = []
  commits = {}

  try:
    cur.execute(
      '''
      SELECT pg_logical_slot_get_changes(%s, NULL, NULL, %s, %s)
      ''', (slot, 'include-timestamp', 'on'))
    draw = cur.fetchall()
  except:
    traceback.print_exc()

  for line in draw:
    logd = {}
    # each line looks like this:
    # ('(0/173BAF8,771,"COMMIT 771 (at 2016-06-03 19:08:10.77748+00)")',)
    log = re.sub('[(^\()(\)$]','',line[0]).split(',')
    logid = log[1]
    logtxt = re.sub('[(^\")(\"$)]','',log[2])
    tokens = re.sub('\[[\w ]+\]','',logtxt).strip().split() 

    # "COMMIT 771 (at 2016-06-03 19:08:10.77748+00)"
    if tokens[0] == 'COMMIT':
      tstamp = ' '.join([tokens[3], tokens[4]])
      uspattern = '(?<=\.)\d+(?=\+.)'
      us = re.search('(?<=\.)\d+(?=\+.)', tstamp).group(0).zfill(6)
      commits[logid] = re.sub('\+\d+$', '', re.sub(uspattern, us, tstamp))

    # "table public.transaction: INSERT: order_date[date]:\'2016-06-03\' order_time[integer]:1010 sales_rep_id[character]:\'1-001\' product_id[character varying]:\'N001\' unit_sold[integer]:137"
    elif tokens[0] == 'table':
      logd['logid'] = logid
      logd['table'] = tokens[1].replace('public.','')
      for t in tokens[3:] :
        logd[t.split(':')[0]] = re.sub('[(^\')(\'$)]','',t.split(':')[1])

    d.append(logd)

  return (commits, d)

def stopreplication(slot):
  # drop slot
  try:
    cur.execute(
      '''
      SELECT pg_drop_replication_slot(%s)
      '''
      , (slot,)) 
    print slot, 'dropped.'
  except:
    None

def usage():
  print 'Usage:'
  print '  ', sys.argv[0], 'slotname', 'interval_in_sec'
  sys.exit(1)

if __name__ == '__main__':
  
  if len(sys.argv) != 3:
    usage()

  slot = sys.argv[1]
  topic = slot
  interval = sys.argv[2]

  try:
       
    con = psycopg2.connect(database='salesbi', user='salesbi') 
    cur = con.cursor()
  
    startreplication(slot)
    producer = KafkaProducer()
  
    while True:
      c, d = getlogs()
  
      for di in d:
        if len(di) == 0:
          continue
        logid = di['logid']
        di['timestamp'] = c[logid]
        producer.send(topic, json.dumps(di))
  
      print str(len(d)), 'messages sent'
      time.sleep(float(interval))

  except KeyboardInterrupt, ke: 
    None
  except:
    traceback.print_exc()
    sys.exit(1)
    
  finally:
    stopreplication(slot)
    if con:
        con.close()

  sys.exit(0)
