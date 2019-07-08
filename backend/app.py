from UTN_Keysight_9917A import VNA
from flask import Flask
from flask import jsonify
from flask_cors import CORS

# myVNA = VNA("TCPIP::10.128.0.206::inst0::INSTR")
myVNA = VNA("Debug")

app = Flask(__name__)
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
