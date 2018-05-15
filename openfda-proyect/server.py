import http.server
import http.client
import json
import socketserver


PORT=8000


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    OPENFDA_API_URL="api.fda.gov"
    OPENFDA_API_EVENT="/drug/event.json"
    OPENFDA_API_DRUG='&search=patient.drug.medicinalproduct:'
    OPENFDA_API_COMPANY='&search=companynumb:'



    def get_index(self):
        html = """
            <html>
                <head>
                    <title>OpenFDA App</title>
                </head>
                <body>
                    <h1>OpenFDA listado </h1>
                    <form method="get" action="listDrugs">
                        <input type = "submit" value="Lista de farmacos">
                        Limite: <input type="text" name="limit" value="1">
                        </input>
                        
                    </form>
                    <form method="get" action="searchDrug">
                        <input type = "submit" value="Busqueda de farmacos">
                        <input type = "text" name="drug"></input>
                        </input>
                    </form>
                    <form method="get" action="listCompanies">
                        <input type = "submit" value="Lista de empresas">
                        Limite: <input type="text" name="limit" value="1">
                        </input>
                    </form>
                    <form method="get" action="listWarnings">
                        <input type = "submit" value="Lista de advertencias">
                        Limite: <input type="text" name="limit" value="1">
                        </input>
                    </form>
                    <form method="get" action="searchCompany">
                        <input type = "submit" value="Busqueda de empresas">
                        <input type = "text" name="company"></input>
                        </input>
                    </form>
                    <body style = 'background-color: lightblue'><html>
                </body>
            </html>
                """
        return html




    def do_GET(self):




        self.send_response(200)


        self.send_header('Content-type','text/html')
        self.end_headers()

        resource = self.path.split("?")
        if len(resource)>1:
            parametros=resource[1]

        else:
            parametros = ""


        if parametros:
            partes_limite = parametros.split("=")
            if partes_limite[0] == "limit":
                limit=int(partes_limite[1])


        else:
            print("No hay parámetro")

        
        if self.path=='/':
            html=self.get_index()
            self.wfile.write(bytes(html, "utf8"))
        elif 'listDrugs' in self.path:
            conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
            conn.request("GET", self.OPENFDA_API_EVENT + "?limit=10")
            r1 = conn.getresponse()
            repos_raw = r1.read().decode("utf8")
            repos = json.loads(repos_raw)
            info = repos['results']
            farmacos = []
            for i in info:
                farmacos += [i['patient']['drug'][0]['medicinalproduct']]

            mensaje = """
                                <html>
                                    <head>
                                        <title>OpenFDA </title>
                                    </head>
                                    <body>
                                    <body style = 'background-color: lightblue'><html>
                                    <h1>Listado de farmacos </h1>
                                        <ul>
                            """
            for obj in farmacos:
                mensaje += "<li>" + obj + "</li>"

            mensaje += """
                                        </ul>
                                    </body>
                                </html>
                            """
            self.wfile.write(bytes(mensaje, "utf8"))


        elif 'listCompanies' in self.path:
            conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
            conn.request("GET", self.OPENFDA_API_EVENT + "?limit=10")
            r1 = conn.getresponse()
            repos_raw = r1.read().decode("utf8")
            repos = json.loads(repos_raw)
            info = repos['results']
            empresas = []
            for i in info:
                empresas += [i['companynumb']]
            mensaje = """
                        <html>
                            <head>
                                <title>OpenFDA </title>
                            </head>
                            <body>
                            <body style = 'background-color: lightblue'><html>
                            <h1>Listado de empresas </h1>
                                <ul>
                    """
            for obj in empresas:
                mensaje += "<li>" + obj + "</li>"

            mensaje += """
                                </ul>
                            </body>
                        </html>
                    """
            self.wfile.write(bytes(mensaje, "utf8"))

        elif 'listWarnings' in self.path:
            advertencias = []
            conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
            conn.request("GET", self.OPENFDA_API_EVENT + "?limit=10")
            r1 = conn.getresponse()
            repos_raw = r1.read().decode("utf8")
            repos = json.loads(repos_raw)
            info = repos['results']

            for i in info:

                if "warnings" in i:
                    advertencias.append([i['warnings']])
                else:
                    advertencias.append("No contiene advertencias")


            mensaje = """
                        <html>
                            <head>
                                <title>OpenFDA </title>
                            </head>
                            <body>
                            <body style = 'background-color: lightblue'><html>
                            <h1>Listado de advertencias </h1>
                                <ul>
                    """
            for obj in advertencias:
                mensaje += "<li>" + obj + "</li>"

            mensaje += """
                                </ul>
                            </body>
                        </html>
                    """
            self.wfile.write(bytes(mensaje, "utf8"))

        elif  'searchDrug' in self.path:
            farmaco=self.path.split('=')[1]
            conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
            conn.request("GET", self.OPENFDA_API_EVENT + "?limit=10" + self.OPENFDA_API_DRUG + farmaco)
            r1 = conn.getresponse()
            repos_raw = r1.read().decode("utf-8")
            repos = json.loads(repos_raw)
            info_search_drug = repos['results']
            farmacos=[]
            for i in info_search_drug:
                farmacos += [i['patient']['drug'][0]['medicinalproduct']]


            mensaje = """
                        <html>
                            <head>
                                <title>OpenFDA </title>
                            </head>
                            <body>
                            <body style = 'background-color: lightblue'><html>
                            <h1>Farmacos buscados </h1>
                                <ul>
                    """
            for obj in farmacos:
                mensaje += "<li>" + obj + "</li>"

            mensaje += """
                                </ul>
                            </body>
                            
                        </html>
                    """
            self.wfile.write(bytes(mensaje, "utf8"))

        elif 'searchCompany' in self.path:
            empresa=self.path.split('=')[1]
            conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
            conn.request("GET", self.OPENFDA_API_EVENT + "?limit=10" + self.OPENFDA_API_COMPANY + empresa)
            r1 = conn.getresponse()
            repos_raw = r1.read().decode("utf-8")
            repo = json.loads(repos_raw)
            info_search_company = repo['results']
            empresas = []
            for i in info_search_company:
                empresas += [i['companynumb']]

            mensaje = """
                                    <html>
                                        <head>
                                            <title>OpenFDA </title>
                                        </head>
                                        <body>
                                        <body style = 'background-color: lightblue'><html>
                                        <h1>Empresas buscadas </h1>
                                            <ul>
                                """
            for obj in empresas:
                mensaje += "<li>" + obj + "</li>"

            mensaje += """
                                            </ul>
                                        </body>
                                    </html>
                                """
            self.wfile.write(bytes(mensaje, "utf8"))

        else:
            self.send_error(404)
            self.send_header('Content-type', 'text/plain; charset = utf-8')
            self.end_headers()
            self.wfile.write("Recurso no encontrado".format(self.path).encode())

        return



socketserver.TCPServer.allow_reuse_address= True

#Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("Sirviendo en el puerto", PORT)
httpd.serve_forever()
