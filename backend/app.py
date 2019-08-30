from UTN_Keysight_9917A import VNA
from flask import Flask, session,redirect, url_for
from flask import jsonify
from flask_cors import CORS
import os
import logging

# Cambiar esta variable a False para produccion
debug = True

app = Flask(__name__)

if debug:
    app.run(debug=True)
    app.logger.setLevel(logging.DEBUG)
    myVNA = VNA("Debug")
else:
    myVNA = VNA("TCPIP::10.128.0.206::inst0::INSTR")

app.config['SERVER_NAME'] = 'vnabackend.com'

# Se genera la clave secreta para el modulo session
app.secret_key = b'\xc0\x1c\x8f\x07\xd9\x1f\xcd\x8dkX\xb8\x94\xe6\xd5\xb5\xaf'

CORS(app)

@app.route("/api/getActualConfig", methods=['GET'])
def getActualConfig():
    value = myVNA.getActualConfig()
    return jsonify(value)

@app.route("/api/getBatteryCharge", methods=['GET'])
def getBatteryCharge():
    value = myVNA.getBatteryCharge()
    return jsonify({'battery': value})

@app.route("/api/getDebugState", methods=['GET'])
def getDebugState():
    return jsonify({'debug':myVNA.debug})

# -------------------------------------------------------
#
# Esta seccion  de funciones se encargan de la rotacion del mutex
#
# -------------------------------------------------------
@app.route("/api/getMutex", methods=['GET'])
def getMutex():
    response = {}
    if "uuid" in session:
        # Usuario ya se conectó una vez
        if "mutex" in session:
            # Usuario ya tiene el mutex
            if not myVNA.checkIfUserIsCurrent(session["uuid"]):
                # Quitar el mutex al usuario
                session.pop("mutex",None)
        else:
            # Usuario no tiene el mutex
            if myVNA.checkIfUserIsCurrent(session["uuid"]):
                # Asignar mutex a usuario
                session["mutex"] = True
    else:
        # Usuario nunca se conectó, crear uuid y agregar a la cola de usuario
        session["uuid"] = myVNA.addNewUser()
        app.logger.debug("New user {0} added.".format(session["uuid"]))
        response["uuid"] = session["uuid"]

    return "OK"

@app.route("/api/destroySession", methods=['POST'])
def destroySession():
    if "uuid" in session:
        myVNA.deleteUser(session["uuid"])
    return "OK"