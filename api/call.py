rom flask_restful import Resource
import serial
import time
import requests
from flask import request

class call(Resource):
    def __init__(self, **kwargs):
        self.serial = kwargs['serial']

    def get(self, phoneNumber, **kwargs):
        self.callFunction(phoneNumber)
        return {'response': 'call to +' + phoneNumber }

    def post(self):
        json_data = request.get_json(force=True)
        phoneNumber = json_data['phone']
        self.callFunction(phoneNumber)
        return {'response': 'call to +' + phoneNumber }

    def callFunction(self, phoneNumber):
        self.serial.write(b"ATH\r")
        time.sleep(0.5)
        phone_number = "ATD+" + phoneNumber + ";\r"
        self.serial.write(phone_number.encode('utf-8'))
        time.sleep(10)
        self.serial.write(b"ATH\r")
