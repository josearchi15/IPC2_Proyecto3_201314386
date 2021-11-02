import datetime, re

class Autorizacion:
    def __init__(self):
        date = datetime.datetime.now()
        self.fecha = str(date.day)+"/"+str(date.month)+"/"+str(date.year)
        self.facturasRecibidas = 0
        self.errores = {
            "NIT_EMISOR":[],
            "NIT_RECEPTOR":[],
            "IVA":[],
            "TOTAL":[],
            "REFERENCIA_DUPLICADA":[]
        }
        self.facturasCorrectas = 0
        self.cantidadEmisores = []
        self.cantidadReceptores = []
        self.ListadoAutorizaciones = list()
        self.aprobaciones = []

    def construccion(self, jsonData): #json enviado del request
        arrFechasTemp = []
        for dte in jsonData["SOLICITUD_AUTORIZACION"]["DTE"]:
            self.facturasRecibidas += 1
            for attr in dte:
                regg = re.search("(\s){2,}", dte[attr])
                if regg:
                    quitar = regg.group()
                    dato = dte[attr]
                    dato = dato.replace(quitar, "").replace("\n", "")
                    dte[attr] = dato

                fecha = re.search("((\d{2})\/){2}\d{4}", dte["TIEMPO"])
                dte["TIEMPO"] = fecha.group()

            dte["NIT_EMISOR"] = nitValido(dte["NIT_EMISOR"]) 
            dte["NIT_RECEPTOR"] = nitValido(dte["NIT_RECEPTOR"])
            
            valor2decimales = "{:.2f}".format(float(dte["VALOR"]))
            dte["VALOR"] = str(valor2decimales)
            iva2decimales = "{:.2f}".format(float(dte["IVA"]))
            dte["IVA"] = str(iva2decimales)
            total2decimales = "{:.2f}".format(float(dte["TOTAL"]))
            dte["TOTAL"] = str(total2decimales)

            valor = float(dte["VALOR"])
            
            iva = float(dte["IVA"])
            iva = "{:.2f}".format(iva)

            ivaEsperado = valor * 0.12
            ivaEsperado = "{:.2f}".format(ivaEsperado)

            total = float(dte["TOTAL"])
            total = "{:.2f}".format(total)

            
            resultado = valor * 1.12
            resultado = "{:.2f}".format(resultado)
            
            
            #  VALIDACIONES DE LOS DATOS
            if len(dte["REFERENCIA"]) > 40: #  Referencia: Maximo 40 Posiciones
                self.errores["REFERENCIA_DUPLICADA"].append(dte["REFERENCIA"])
            elif dte["REFERENCIA"] in self.errores["NIT_EMISOR"]:  #si la referencia este duplicada
                self.errores["REFERENCIA_DUPLICADA"].append(dte["REFERENCIA"])
            elif len(dte["NIT_EMISOR"]) > 21 or dte["NIT_EMISOR"] == "Invalido": #valida si el nit emisor esta correcto
                self.errores["NIT_EMISOR"].append(dte["NIT_EMISOR"])
            elif len(dte["NIT_RECEPTOR"]) > 21 or dte["NIT_RECEPTOR"] == "Invalido": #valida si el nit receptor esta correcto
                self.errores["NIT_RECEPTOR"].append(dte["NIT_RECEPTOR"])
            elif total != resultado:   # si el total esta incorrecto
                self.errores["TOTAL"].append(dte["TOTAL"])
            elif iva != ivaEsperado:   # si el total esta correcto pero el iva no
                self.errores["IVA"].append(dte["IVA"])
            else:
                if dte["NIT_EMISOR"] not in self.cantidadEmisores:
                    self.cantidadEmisores.append(dte["NIT_EMISOR"])
                if dte["NIT_RECEPTOR"] not in self.cantidadReceptores:
                    self.cantidadReceptores.append(dte["NIT_RECEPTOR"])
                self.ListadoAutorizaciones.append(dte)
        self.aprobar()
    
    def aprobar(self):
        for dte in self.ListadoAutorizaciones:
            objDte = {
                "NIT_EMISOR": dte["NIT_EMISOR"],
                "REFERENCIA": dte["REFERENCIA"]
            }
            self.aprobaciones.append(objDte)

    def consultaDatos(self):
        objInfo = {
            "AUTORIZACION":{
                "FECHA": self.fecha,
                "FACTURAS_RECIBIDAS": self.facturasRecibidas,
                "ERRORES":{
                    "NIT_EMISOR":len(self.errores["NIT_EMISOR"]),
                    "NIT_RECEPTOR":len(self.errores["NIT_RECEPTOR"]),
                    "IVA":len(self.errores["IVA"]),
                    "TOTAL":len(self.errores["TOTAL"]),
                    "REFERENCIA_DUPLICADA":len(self.errores["REFERENCIA_DUPLICADA"]),
                },
                "FACTURAS_CORRECTAS":len(self.ListadoAutorizaciones),
                "CANTIDAD_EMISORES":len(self.cantidadEmisores),
                "CANTIDAD_RECEPTORES":len(self.cantidadReceptores),
                "LISTADO_ATORIZACIONES": self.aprobaciones,
                "TOTAL_APROBACIONES":len(self.ListadoAutorizaciones)
            } 

        }
        return objInfo


def nitValido(nit):
    posicion = len(nit) -1
    suma = 0
    multiplicador = 2
    while posicion >= 0:
        if multiplicador > 7:
            multiplicador = 2
            valor = int(nit[posicion]) * multiplicador
            suma += valor
            posicion -= 1
            multiplicador += 1
        else:
            valor = int(nit[posicion]) * multiplicador
            suma += valor
            posicion -= 1
            multiplicador += 1
    modal = suma % 11
    identificador = 11 - modal
    # print("Valor identificador: "+ str(identificador))
    if identificador < 10:
        nit = nit+"K"
    elif identificador >= 10:
        nit = "Invalido"
    return nit