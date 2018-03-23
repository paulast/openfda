import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)

repo = repos["results"][0]
print("El id del medicamento es", repo["id"])
print("El propósito del producto es", repo["purpose"])
print("El nombre del fabricante es", repo["openfda"]["manufacturer_name"])

    

