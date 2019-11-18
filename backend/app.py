from UTN_Keysight_9917A import VNA
from flask import Flask, session,redirect, url_for, request, abort
from flask import jsonify
from flask_cors import CORS
import os
import logging
import threading

# Semaforo para evitar el acceso concurrente al VNA
sem = threading.Semaphore()

# Cambiar esta variable a False para produccion
debug = True

#mutex = False

app = Flask(__name__)

#app.run(debug=debug, port=5000, host="0.0.0.0")

if debug:
    app.logger.setLevel(logging.DEBUG)
    myVNA = VNA("Debug")
else:
    myVNA = VNA("TCPIP::10.128.0.206::inst0::INSTR")

CORS(app,supports_credentials=True)

@app.route("/api/getActualConfig", methods=['GET'])
def getActualConfig():
    sem.acquire()
    value = myVNA.getActualConfig()
    sem.release()
    app.logger.debug(value)
    return jsonify(value)

@app.route("/api/getBatteryCharge", methods=['GET'])
def getBatteryCharge():
    sem.acquire()
    value = myVNA.getBatteryCharge()
    sem.release()
    return jsonify({'battery': value})

@app.route("/api/getDebugState", methods=['GET'])
def getDebugState():
    return jsonify({'debug':myVNA.debug})

@app.route("/api/setTraceNewFreq", methods=['POST'])
def setTraceNewFreq():
    value = request.json
    app.logger.debug(value)
    sem.acquire()
    myVNA.selectTrace(value['selectedTrace'])
    myVNA.setStartFrequency(value['minFreq'])
    myVNA.setStopFrequency(value['maxFreq'])
    sem.release()
    mutex = False
    return jsonify({})

@app.route("/api/setSweep", methods=['POST'])
def setSweep():
    value = request.json
    app.logger.debug(value)
    sem.acquire()
    myVNA.setSweepTime(value['sweepTime'])
    myVNA.setSweepResolution(value['sweepResolution'])
    sem.release()
    return jsonify({})

@app.route("/api/setScale", methods=['POST'])
def setScale():
    value = request.json
    app.logger.debug(value)
    sem.acquire()
    myVNA.setYPDiv(value['selectedTrace'],value['newPDiv'])
    sem.release()
    return jsonify({})

@app.route("/api/setIFBW", methods=['POST'])
def setIFBW():
    value = request.json
    app.logger.debug(value)
    sem.acquire()
    myVNA.setIFBW(value['ifbw'])
    sem.release()
    return jsonify({})

if __name__ == '__main__':
    app.run(debug=debug,host='0.0.0.0',port=5000)
