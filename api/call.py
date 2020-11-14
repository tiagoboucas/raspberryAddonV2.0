from flask_restful import Resource
import serial
import time

class call(Resource):
    def init(self, **kwargs):
        self.serial = kwargs['serial']

    def get(self, phoneNumber):
        self.serial.write(b"ATH\r")
        time.sleep(0.5)
        phone_number = "ATD+" + phoneNumber + ";\r"
        self.serial.write(phone_number.encode('utf-8'))
        time.sleep(10)
        self.serial.write(b"ATH\r")
        return {'response': 'call to +' + phoneNumber }