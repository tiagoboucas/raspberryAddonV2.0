from flask import Flask, request
from flask_restful import Resource, Api
from api.call import call
from api.sms import sms
import serial
import time
import threading

app = Flask(__name__)
api = Api(app)

PORT = '/dev/ttyUSB3'
BAUDRATE = 115200

ser = serial.Serial(PORT, BAUDRATE, timeout = 5)

from gsmmodem.modem import GsmModem
from gsmmodem.exceptions import InterruptedException, CommandError, TimeoutException


def handleSms(sms):
    global ser
    print(u'== SMS message received ==\nFrom: {0}\nTime: {1}\nMessage:\n{2}\n'.format(sms.number, sms.time, sms.text))

try:
    modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
except e:
    print(e)
    modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
    
def read_messages(name):
    try:
        while 1:
           time.sleep(3)
    except e:
        print(e)
    finally:
        modem.close()

api.add_resource(call, '/call', '/call/<string:phoneNumber>', resource_class_kwargs={ 'serial': ser, 'modem': modem })
api.add_resource(sms, '/sms', '/sms/<string:phoneNumber>/<string:message>', resource_class_kwargs={ 'serial': ser, 'modem': modem })

if __name__ == '__main__':
    modem.smsTextMode = False
    modem.connect()
    print('start...')
    x = threading.Thread(target=read_messages, args=(1,))
    x.start()
    app.run(port=4000)

