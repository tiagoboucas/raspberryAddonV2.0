
from flask import Flask, request
from flask_restful import Resource, Api
from api.call import call
from api.sms import sms
import serial
import time
import threading
from requests import get, post

app = Flask(__name__)
api = Api(app)

PORT = '/dev/ttyUSB3'
BAUDRATE = 115200

ser = serial.Serial(PORT, BAUDRATE, timeout = 5)

from gsmmodem.modem import GsmModem
from gsmmodem.exceptions import InterruptedException, CommandError, TimeoutException

def handleSms(sms):
    global ser
    global modem
    url = 'http://localhost:3000/message/action'
    req = post(url, { 'phone_number': sms.number, 'message': sms.text, 'time': sms.time },headers={})
    print(u'== SMS message received ==\nFrom: {0}\nTime: {1}\nMessage:\n{2}\n'.format(sms.number, sms.time, sms.text))
    modem.deleteMultipleStoredSms(4)
try:
    modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
except Exception as e:
    print(e)
    modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)


api.add_resource(call, '/call', '/call/<string:phoneNumber>', resource_class_kwargs={ 'serial': ser, 'modem': modem })
api.add_resource(sms, '/sms', '/sms/<string:phoneNumber>/<string:message>', resource_class_kwargs={ 'serial': ser, 'modem': modem })

if __name__ == '__main__':
    try:
       modem.smsTextMode = False
       modem.connect()
       print('start...')
       app.run(port=4000)
    except:
       print('Exception')

