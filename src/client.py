import socketio


sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

def emit(event, data):
    if sio.connected:
        print('Emit', event)
        sio.emit(event, data)
    else:
        print('Not connected to server. Skipping', event)

try:
    sio.connect('ws://192.168.1.42:4000')
except socketio.exceptions.ConnectionError:
    print('Cannot connect to the server. Continuing...')
