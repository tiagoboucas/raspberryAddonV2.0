from flask_restful import Resource
import serial
import time

class sms(Resource):
    def init(self, **kwargs):
        self.serial = kwargs['serial']

    def get(self, phoneNumber, message):
        self.serial.write(b'ATZ\r')
        time.sleep(0.5)
        self.serial.write(b'AT+CMGF=1\r')
        time.sleep(0.5)
        self.serial.write(b'AT+CMGS="+' + phoneNumber.encode() + b'"\r')
        time.sleep(0.5)
        self.serial.write(message.encode() + b"\r")
        time.sleep(0.5)
        self.serial.write(bytes([26]))
        return {'response': 'sms to +' + phoneNumber}