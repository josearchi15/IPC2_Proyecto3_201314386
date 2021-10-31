import json, re
from os import replace
from flask import Flask, jsonify, request
from autorizacion import Autorizacion

autorizacion = Autorizacion()

app = Flask(__name__)

@app.route('/')
def ping():
    return jsonify({"menssage":"Server On!!!"})

@app.route('/api/procesar', methods=['POST'])
def procesar():
    print("\n Procesando....")
    
    autorizacion.construccion(request.json)
        
    print(request.json["SOLICITUD_AUTORIZACION"]["DTE"])

    return jsonify(request.json)

@app.route('/api/consultaDatos')
def consultaDatos():
    print(autorizacion.ListadoAutorizaciones)
    return jsonify({"menssage":"Server On!!!"})

@app.route('/api/resumenRango')
def resumenRago():
    return jsonify({"menssage":"Server On!!!"})

@app.route('/api/resumenIva')
def resumenIva():
    return jsonify({"menssage":"Server On!!!"})



if __name__ == '__main__':
    app.run(debug=True, port=4000)