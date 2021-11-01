from django.http import response
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
import requests
import json
import xmltodict

BASE_API_URL = "http://127.0.0.1:4000/api/"

# Create your views here.
def home(request):
    return render(request, "home.html", {})

def carga(request):
    if request.method == "POST":
        print("Enviando archivo...")

        fileUploaded = request.FILES["document"]
        # fileData = fileUploaded.read().decode("utf-8")
        # print(fileData)
        data_dict = xmltodict.parse(fileUploaded)
        fileUploaded.close()
        # print(data_dict)
        json_data = json.dumps( data_dict )
        json_object = json.loads(json_data)
        # print(json_object)

        response = requests.post(BASE_API_URL+"procesar", json=json_object)
        print("Enviando archivo...")

        print(response.json())

    return render(request, "cargaArchivo.html", {})
    # return redirect("consulta-datos")

def consultaDatos(request):
    response = requests.get(BASE_API_URL+"consultaDatos")
    print(response.json)
    
    return render(request, "consultaDatos.html", {"texto":response.json})
    