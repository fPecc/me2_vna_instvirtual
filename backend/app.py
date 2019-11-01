from UTN_Keysight_9917A import VNA
from flask import Flask, session,redirect, url_for, request
from flask import jsonify
from flask_cors import CORS
import os
import logging

# Cambiar esta variable a False para produccion
debug = True

app = Flask(__name__)

app.run(debug=debug, port=5000, host="0.0.0.0")

if debug:
    app.logger.setLevel(logging.DEBUG)
    myVNA = VNA("Debug")
else:
    myVNA = VNA("TCPIP::10.128.0.206::inst0::INSTR")

# Se genera la clave secreta para el modulo session
app.config["SECRET_KEY"] = b'\xc0\x1c\x8f\x07\xd9\x1f\xcd\x8dkX\xb8\x94\xe6\xd5\xb5\xaf'

CORS(app,supports_credentials=True)

@app.route("/api/getActualConfig", methods=['GET'])
def getActualConfig():
    value = myVNA.getActualConfig()
    app.logger.debug(value)
    return jsonify(value)

@app.route("/api/getBatteryCharge", methods=['GET'])
def getBatteryCharge():
    value = myVNA.getBatteryCharge()
    return jsonify({'battery': value})

@app.route("/api/getDebugState", methods=['GET'])
def getDebugState():
    return jsonify({'debug':myVNA.debug})

@app.route("/api/setTraceNewFreq", methods=['POST'])
def setTraceNewFreq():
    value = request.json
    app.logger.debug(value)
    myVNA.selectTrace(value['selectedTrace'])
    myVNA.setStartFrequency(value['minFreq'])
    myVNA.setStopFrequency(value['maxFreq'])
    return jsonify({})

@app.route("/api/setSweep", methods=['POST'])
def setSweep():
    value = request.json
    app.logger.debug(value)
    # TODO: llamar a la funcion de la libreria correspondiente
    myVNA.setSweepTime(value['sweepTime'])
    return jsonify({})

@app.route("/api/setScale", methods=['POST'])
def setScale():
    value = request.json
    app.logger.debug(value)
    # TODO: llamar a la funcion de la libreria correspondiente
    myVNA.selectTrace(value['selectedTrace'])
    return jsonify({})

# -------------------------------------------------------
#
# Esta seccion  de funciones se encargan de la rotacion del mutex
#
# -------------------------------------------------------
@app.route("/api/getMutex", methods=['GET'])
def getMutex():
    response = {'mutex': False}
    if "uuid" in session:
        # Usuario ya se conectó una vez
        if "mutex" in session:
            # Usuario ya tiene el mutex
            if not myVNA.checkIfUserIsCurrent(session["uuid"]):
                # Quitar el mutex al usuario
                session.pop("mutex",None)
            else:
                response = {'mutex': True}
        else:
            # Usuario no tiene el mutex
            if myVNA.checkIfUserIsCurrent(session["uuid"]):
                # Asignar mutex a usuario
                session["mutex"] = True
                response = {'mutex': True}
    else:
        # Usuario nunca se conectó, crear uuid y agregar a la cola de usuario
        session["uuid"] = myVNA.addNewUser()
        session["mutex"] = True
        # app.logger.debug("New user {0} added.".format(session["uuid"]))
        app.logger.debug(session)
        # response["uuid"] = session["uuid"]
        session.modified = True

    return jsonify(response)

@app.route("/api/destroySession", methods=['POST'])
def destroySession():
    app.logger.debug(session)
    if "uuid" in session:
        app.logger.debug(session)
        myVNA.deleteUser(session["uuid"])
    return "OK"
