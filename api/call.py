from flask_restful import Resource
import serial
import time
import requests
from flask import request

class call(Resource):
    def __init__(self, **kwargs):
        self.serial = kwargs['serial']
        self.modem = kwargs['modem']

    def get(self, phoneNumber, **kwargs):
        self.callFunction(phoneNumber)
        return {'response': 'call to +' + phoneNumber }

    def post(self):
        json_data = request.get_json(force=True)
        phoneNumber = json_data['phone']
        self.callFunction(phoneNumber)
        return {'response': 'call to +' + phoneNumber }

    def callFunction(self, phoneNumber):
        try:
           self.modem.smsTextMode = False
           call = self.modem.dial(phoneNumber)
           time.sleep(8)
           self.serial.write(b"ATH\r\n")
           self.modem.smsTextMode = True
        finally:
           self.serial.write(b"ATH")
           time.sleep(0.5)
           self.serial.write(b"ATH0;\r")
           self.modem.smsTextMode = True

