import json
from os import replace
from flask import Flask, jsonify, request
import re

from werkzeug.wrappers import response

app = Flask(__name__)

@app.route('/')
def ping():
    return jsonify({"menssage":"Server On!!!"})

@app.route('/api/procesar', methods=['POST'])
def procesar():
    print("\n Procesando....")
    # print(request.json["SOLICITUD_AUTORIZACION"]["DTE"][2])
    
    #Formateando nuestros datos
    for dte in request.json["SOLICITUD_AUTORIZACION"]["DTE"]:
        for attr in dte:
            regg = re.search("(\s){2,}", dte[attr])
            if regg:
                quitar = regg.group()
                dato = dte[attr]
                dato = dato.replace(quitar, "").replace("\n", "")
                dte[attr] = dato

        fecha = re.search("((\d{2})\/){2}\d{4}", dte["TIEMPO"])
        dte["TIEMPO"] = fecha.group()
        
    print(request.json["SOLICITUD_AUTORIZACION"]["DTE"])

    return jsonify(request.json)

@app.route('/api/consultaDatos')
def consultaDatos():
    return jsonify({"menssage":"Server On!!!"})

@app.route('/api/resumenRango')
def resumenRago():
    return jsonify({"menssage":"Server On!!!"})

@app.route('/api/resumenIva')
def resumenIva():
    return jsonify({"menssage":"Server On!!!"})



if __name__ == '__main__':
    app.run(debug=True, port=4000)