from flask import Flask, request
from flask_restful import Resource, Api
from api.call import call
from api.sms import sms
import serial
import time
import threading

app = Flask(__name__)
api = Api(app)

ser = serial.Serial("/dev/ttyAMA0", baudrate = 9600, timeout = 5)

def read_messages(name):
    while(1):
        time.sleep(1)
        reply = ser.read(ser.inWaiting())
        if len(reply) > 0:
            print(reply)
        
api.add_resource(call, '/call/<string:phoneNumber>', resource_class_kwargs={ 'serial': ser })
api.add_resource(sms, '/sms/<string:phoneNumber>/<string:message>', resource_class_kwargs={ 'serial': ser })

if __name__ == '__main__':
    ser.write(b"AT+CMGF=1\r")
    time.sleep(0.5)
    ser.write(b"AT+CNMI=2,2,0,0,0\r")
    time.sleep(0.5)
    print('start...')
    x = threading.Thread(target=read_messages, args=(1,))
    x.start()
    app.run(port=4000)
