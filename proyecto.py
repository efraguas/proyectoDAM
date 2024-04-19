from bs4 import *
import requests
import json
from pymongo import MongoClient

# definimos la url a descargar
url = "https://www.latiendadeldentista.com/65_master-surgical-sl?id_manufacturer=65&n=1732"

# Descarga del contenido HTML
response = requests.get(url)
html = response.content

# Parseo del HTML con BeautifulSoup
soup = BeautifulSoup(html, "lxml")

# Búsqueda de las categorías

lista_productos = soup.find('div', class_="product_list grid row")
productos = soup.find_all('div', class_="product-container")
precio_producto = soup.find_all('div', class_="content-price")

# iterar sobre el documento para extraer la informacion (nombre producto y precio)
lista_nombres = []
lista_precios = []
lista_marca = []
datos_productos = []

for items in productos:
    precio = items.find('span', class_="price product-price").text
    texto_producto = items.find('a', class_="product-name").text
    marca = items.find('span', class_="manufacturer-name").text
    productos = {
        "nombre producto": texto_producto.replace('\n', '').replace('\t', ''),
        "marca": marca.replace('\n', '').replace('\t', ''),
        "precio": float(precio.replace('\n', '').replace('\t', '').replace(" €+IVA", '').replace(",", '.'))
    }
    lista_marca.append(marca.replace('\n', '').replace('\t', ''))
    lista_nombres.append(texto_producto.replace('\n', '').replace('\t', ''))
    lista_precios.append(precio.replace('\n', '').replace('\t', ''))
    datos_productos.append(productos)


# Almacenar en JSON
with open("productos.json", "w") as JSON:
    json.dump(datos_productos, JSON)

# Almacenar en la colecccion de MongoDB

cliente = MongoClient('mongodb://localhost:27017')
db = cliente['Materiales_odontologia']
coleccion = db['materiales']
coleccion.insert_many(datos_productos)
print("datos añadidos correctamente")
