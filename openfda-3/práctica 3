import socket
import http.client
import json


IP = "192.168.1.1"
PORT = 8020
MAX_OPEN_REQUESTS = 5

def process_client(clientsocket):
    """Funcion que atiende al cliente. Lee su peticion (aunque la ignora)
       y le envia un mensaje de respuesta en cuyo contenido hay texto
       en HTML que se muestra en el navegador"""

    
    mensaje_solicitud = clientsocket.recv(1024)

    contenido = """
      <!doctype html>
      <html>
      <body style='background-color: blue'>
        <h1>Hola!</h2>
        <p>Estos son los 10 medicamentos</p>
      </body>
      </html>
    """
    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?limit=10", None, headers)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    repos_raw = r1.read().decode("utf-8")
    conn.close()

    repos = json.loads(repos_raw)

    for i in range(len(repos["results"])):
        info=repos["results"][i]

    linea_inicial = "HTTP/1.1 200 OK\n"
    cabecera = "Content-Type: text/html\n"
    cabecera += "Content-Length: {}\n".format(len(str.encode(contenido)))

  
    mensaje_respuesta = str.encode(linea_inicial + cabecera + "\n" + contenido + info["id"])
    clientsocket.send(mensaje_respuesta)
    clientsocket.close()


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    
    serversocket.bind((IP, PORT))
    serversocket.listen(MAX_OPEN_REQUESTS)

    
    while True:
        
        print("Esperando clientes en IP: {}, Puerto: {}".format(IP, PORT))
        (clientsocket, address) = serversocket.accept()

        print("  Peticion de cliente recibida. IP: {}".format(address))
        process_client(clientsocket)

except socket.error:
    print("Problemas usando el puerto {}".format(PORT))
    print("Lanzalo en otro puerto (y verifica la IP)")
