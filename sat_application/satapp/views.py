from django.http import response
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from matplotlib import image
import requests
import json
import xmltodict
from .utils import get_plot

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
        print(request.POST['start'])
    
        xval = [80, 85, 90, 95, 100, 105, 110, 115, 120, 125]
        yval = [240, 250, 260, 270, 280, 290, 300, 310, 320, 330]
        chart = get_plot(xval, yval)
    else:
        chart = None
        
    return render(request, "graficaFecha.html", {'chart':chart})