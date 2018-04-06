import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=10", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
#Hasta este apartado el código es igual al del primer ejercicio, a excepción de la función "limit", utilizada para
#conseguir la información de los diez primeros medicamentos, en lugar de uno solo.
#Con un bucle for iteramos sobre la información que aparece en "results"
#de cada medicamento.
for i in range(len(repos["results"])):
    #En la variable info guardamos esta información de cada medicamento.
    info=repos["results"][i]
    #Imprimimos el id de cada medicamento tal y como pide el ejercicio.
    print("La id del medicamento es", info["id"])







