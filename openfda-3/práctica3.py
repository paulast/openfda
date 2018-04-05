import http.client
import json
import http.server
import socketserver


PORT = 8020


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
    
    
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    
    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = "<html><body>"
        
        if info["openfda"]:
            print("El nombre del medicamento es", info["openfda"]["generic_name"][0])

        
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
