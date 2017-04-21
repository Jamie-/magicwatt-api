#!/usr/bin/python
from flask import Flask
import smbus
import struct
import json

#
# Setup
#

SENSOR_ADDR = 0x04
bus = smbus.SMBus(1) # Change to 0 on older Pis

app = Flask(__name__)

#
# API Endpoints
#

# Main
@app.route('/')
def index():
  return app.send_static_file('index.html')

# Hello World
@app.route('/hello', methods=['GET'])
def hello():
  data = {}
  data['message'] = "Hello, world!"
  return json.dumps(data)

# Current Draw
@app.route('/current', methods=['GET'])
def getCurrent():
  data = {}
  try:
    raw = bus.read_word_data(SENSOR_ADDR, 0)
    i = struct.unpack('>h', struct.pack('<H', raw))[0] / 256.0
    data['current'] = "%d" % (i)
  except Exception as e:
    app.logger.error("Unable to read data from I2C line, {}".format(e))
    data = buildJSONError(100, str(e))
  return json.dumps(data)

#
# Errors
#

# 404 Not Found
@app.errorhandler(404)
def errorPageNotFound(e):
  return json.dumps(buildJSONError(404, "Page not found."))

# 403 Forbidden
@app.errorhandler(403)
def errorForbidden(e):
  return json.dumps(buildJSONError(403, "Forbidden."))

# 410 Gone
@app.errorhandler(410)
def errorGone(e):
  return json.dumps(buildJSONError(410, "Gone."))

# 500 Internal Server Error
@app.errorhandler(500)
def errorInternalServerError(e):
  return json.dumps(buildJSONError(500, "Internal server error."))

# JSON Error Builder
def buildJSONError(code, message):
  error = {}
  error['code'] = code
  error['message'] = message
  data = {}
  data['error'] = error
  return data

#
# Main
#

if __name__ == '__main__':
  app.run(host='0.0.0.0')
