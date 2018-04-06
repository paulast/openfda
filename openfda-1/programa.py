import http.client
import json


headers = {'User-Agent': 'http-client'}

#Ahora nos conectaremos con la página api de fda para poder descargarnos la información del medicamento.
conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
#Almacenamos la información en la variable r1.
r1 = conn.getresponse()
print(r1.status, r1.reason)
#Decodificamos la información obtenida para poder leerlo correctamente (nosotros somos el cliente, por eso se decodifica la información).
repos_raw = r1.read().decode("utf-8")
conn.close()
#En la variable repos guardamos toda la información del archivo descargado y decodificado.
repos = json.loads(repos_raw)

#La variable repo la asociamos solamente a la información que aparece en el apartado "results",
#que es el que nos interesa.
repo = repos["results"][0]
#Imprimimos por pantalla la información que nos indican en el ejercicio. 
print("El id del medicamento es", repo["id"])
print("El propósito del producto es", repo["purpose"][0])
print("El nombre del fabricante es", repo["openfda"]["manufacturer_name"][0])

    


