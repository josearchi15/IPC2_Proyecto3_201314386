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

    # json_formatted_str = json.dumps(request.json, indent=2)    
    # print(json_formatted_str)
    autoriacionesJson = json.dumps(autorizacion.ListadoAutorizaciones, indent=2)
    print(autoriacionesJson)

    return jsonify(request.json)

@app.route('/api/consultaDatos', methods=["GET"])
def consultaDatos():
    # # print(autorizacion.consultaDatos())
    # json_formatted_str = json.dumps(autorizacion.consultaDatos(), indent=2)
    # print(json_formatted_str)
    return jsonify(autorizacion.consultaDatos())


@app.route('/api/resumenRango', methods=["GET"])
def resumenRago():
    return jsonify({"menssage":"Server On!!!"})

@app.route('/api/resumenIva')
def resumenIva():
    return jsonify({"menssage":"Server On!!!"})



if __name__ == '__main__':
    app.run(debug=True, port=4000)