import http.client
import json
import http.server
import socketserver

PORT = 8011
#Creamos una lista que nos servirá de ayuda más adelante.
nombre = list()

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=10", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

#Al igual que antes bajamos y decodificamos la información de cada medicamento.
repos = json.loads(repos_raw)
#De nuevo utilizamos un bucle for para conseguir la información de los diez medicamentos.
for i in range(len(repos["results"])):
    info = repos["results"][i]
    #Si el medicamento contiene el apartado openfda, añadimos a la lista vacía de antes el nombre
    #genérico del medicamento.
    if info["openfda"]:
        nombre.append(info["openfda"]["generic_name"][0])


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        #Envía una respuesta de OK
        self.send_response(200)
        #Indica que el contenido será html.
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        #Escribimos el contenido de nuestra página html.
        mensaje = "<body style = 'background-color: lightblue'><html>"
        mensaje += "<h1><b>Los nombres de los 10 medicamentos son:</b></h1>"
        mensaje += "<h2>El nombre del segundo medicamento no aparece indicado</h2>"
        
        for a in nombre:
            mensaje += a + "<br>"

        mensaje += "</body>"
        mensaje += "</html>"
        
        #Volvemos a codificar el mensaje para mandarlo codificado (en este momento yo soy el servidor)
        self.wfile.write(bytes(mensaje, "utf8"))
        return


Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("Sirviendo en puerto: {}".format(PORT))

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("Servidor detenido")
    httpd.server_close()

