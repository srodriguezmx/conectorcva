import xml.etree.ElementTree as ET
import pandas as pd
import requests

num_cliente = input("Introduce tu número de cliente CVA: ")
clave_producto = input("Introduce la clave de producto de CVA: ")

def loadRSS():

 	# url from the cva.
    url = f"https://www.grupocva.com/catalogo_clientes_xml/lista_precios.xml?cliente={num_cliente}&marca=%&grupo=%&clave={clave_producto}&codigo=%"

 	# Creating a response from the url. 
    resp = requests.get(url)

 	# Save xml to file
    with open('cvaInventario.xml', 'wb') as f:
 	    f.write(resp.content)
 		
# Generate xml tree 
def parseXML(xmlfile):
	tree = ET.parse(xmlfile)
	root = tree.getroot()

 # Add and id to each item 
	id = 1
	for item in tree.findall('item'):
		item.set('id', str(id))
		id += 1  

	tree.write('cvaInventario.xml')

	# Create a CSV
	cols = ["clave", "descripcion", "precio", "imagen"]
	rows = []

	for item in root:
		numero = root.get("id")
		clave = item.find("clave").text
		descripcion = item.find("descripcion").text
		precio = item.find("precio").text 
		imagen = item.find("imagen").text

		rows.append({
			"id": numero, 
			"clave": clave,
			"descripcion": descripcion,
			"precio": precio,
			"imagen": imagen
			})

	df = pd.DataFrame(rows, columns=cols)

	df.to_csv("cvaInventario.csv")

loadRSS()
parseXML('cvaInventario.xml')
