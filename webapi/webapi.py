#!/usr/bin/env python

import eventlet
eventlet.monkey_patch()

import time, json
from kafka import KafkaConsumer
from threading import Thread
from flask import Flask, render_template, session, request
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from consumer import SalesConsumer
from flask_moment import Moment

async_mode = 'eventlet'
app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None

def background_thread():
    sc = SalesConsumer('transaction_slot')
    sc.getrefs()
    for msg in sc.getconsumer():
      if len(msg.value) == 0:
        continue
      sc.getsales(msg)
      d = sc.sales
      try:
        socketio.emit('update',
                      {'data': json.dumps(d)},
                      namespace='', broadcast=True)
      except Exception, e:
        print str(e) 
      print 'emitted'
      time.sleep(1)
    
@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()
    return render_template('dashboard.html')

@socketio.on('connected', namespace='')
def connected():
    emit('status',
         {'status':'Connected.'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)
