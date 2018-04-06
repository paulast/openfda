import http.client
import json
import http.server
import socketserver

PORT = 8011
nombre = list()

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=10", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
for i in range(len(repos["results"])):
    info = repos["results"][i]
    if info["openfda"]:
        nombre.append(info["openfda"]["generic_name"][0])


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        mensaje = "<body style = 'background-color: lightblue'><html>"
        mensaje += "<b>Los nombres de los 10 medicamentos son:</b><br>"

        for a in nombre:
            mensaje += a + "<br>"

        mensaje += "</body>"
        mensaje += "</html>"

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

