#!/usr/bin/python
from flask import Flask
import smbus

SENSOR_ADDR = 0x04
bus = smbus.SMBus(1) # Change to 0 on older Pis

app = Flask(__name__)

@app.route('/')
def index():
  return app.send_static_file('index.html')

@app.route('/hello', methods=['GET'])
def hello():
  return "Hello, world!"

@app.route('/current', methods=['GET'])
def getCurrent():
  try:
    return "{}".format(bus.read_word_data(SENSOR_ADDR, 0))
  except Exception as e:
    app.logger.error("Unable to read data from I2C line, {}".format(e))
    return "Error: 100"

if __name__ == '__main__':
  app.run(host='0.0.0.0')
