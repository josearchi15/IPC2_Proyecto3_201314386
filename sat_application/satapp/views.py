from django.http import response
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from matplotlib import image
import requests
import json
import xmltodict
from .utils import get_plot, toDate

BASE_API_URL = "http://127.0.0.1:4000/api/"

# Create your views here.
def home(request):
    return render(request, "home.html", {})

def carga(request):
    if request.method == "POST":
        print("Enviando archivo...")

        fileUploaded = request.FILES["document"]
        data_dict = xmltodict.parse(fileUploaded)
        fileUploaded.close()
        json_data = json.dumps( data_dict )
        json_object = json.loads(json_data)

        response = requests.post(BASE_API_URL+"procesar", json=json_object)
        print("Enviando archivo...")

        print(response.json())

    return render(request, "cargaArchivo.html", {})

def consultaDatos(request):
    response = requests.get(BASE_API_URL+"consultaDatos")
    json_formatted_str = json.dumps(response.json(), indent=2)
    print(json_formatted_str)
    print(response.json)
    
    return render(request, "consultaDatos.html", {"texto":json_formatted_str})
    
def graficaFechas(request):
    if request.method == "POST":
        start = toDate(request.POST['start'], "-")
        end = toDate(request.POST['end'], "-")

        data = {'start':str(start), 'end':str(end), 'nit':request.POST['nit']}

        response = requests.get(BASE_API_URL+"resumenRango", json=data)
        print(response.json())
        # imagen movimientos Receptor
        xval = response.json()["receptor"]["nits"]
        yval = response.json()["receptor"]["movimientos"]
        chart = get_plot(xval, yval, "NIT "+data['nit'], "Fecha", "Movimientos")

        # imagen movimientos Emisor
        xval1 = response.json()["emisor"]["nits"]
        yval1 = response.json()["emisor"]["movimientos"]
        chart2 = get_plot(xval1, yval1, "NIT "+data['nit'], "Fecha", "Movimientos")
    else:
        chart = None
        chart2 = None
        
    return render(request, "graficaFecha.html", {'chart':chart, 'chart2':chart2})