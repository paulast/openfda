import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?search=substance_name:aspirin&limit=100", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)

for i in range(len(repos["results"])):
    info=repos["results"][i]
    print("El nombre del fabricante es", info["openfda"]["manufacturer_name"][0])
