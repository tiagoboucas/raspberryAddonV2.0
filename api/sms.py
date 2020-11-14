from flask_restful import Resource
from flask import request
import serial
import time

class sms(Resource):
    def __init__(self, **kwargs):
        self.serial = kwargs['serial']

    def get(self, phoneNumber, message):
        self.sendMessage(phoneNumber, message)
        return {'response': 'sms to +' + phoneNumber}

    def post(self):
        json_data = request.get_json(force=True)
        phoneNumber = json_data['phone']
        message = json_data['message']
        self.sendMessage(phoneNumber, message)
        return {'response': 'sms to +' + phoneNumber}

    def sendMessage(self, number, message):
        self.serial.write(b'ATZ\r')
        time.sleep(0.5)
        self.serial.write(b'AT+CMGF=1\r')
        time.sleep(0.5)
        self.serial.write(b'AT+CMGS="+' + number.encode() + b'"\r')
        time.sleep(0.5)
        self.serial.write(message.encode() + b"\r")
        time.sleep(0.5)
        self.serial.write(bytes([26]))
        self.serial.write(b"AT+CMGF=1\r")
        time.sleep(0.5)
        self.serial.write(b"AT+CNMI=2,2,0,0,0\r")
        time.sleep(0.5)
