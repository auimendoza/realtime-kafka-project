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

async_mode = 'eventlet'
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None

def background_thread():
    consumer = KafkaConsumer('transaction_slot')
    for msg in consumer:
      d = msg.value
      try:
        socketio.emit('update',
                      {'type': 'data', 'data': json.dumps(d)},
                      namespace='')
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
    emit('update',
         {'type': 'status', 'status':'Connected.'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)
