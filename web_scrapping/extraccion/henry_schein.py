import time

from pymongo import MongoClient
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Funcion para eliminar simbolo de euro del texto precio y puntos separadores excepto
# decimal
def convertir_precio(precio):
    # Eliminar espacios en blanco al principio y al final
    precio = precio.strip().replace('€', '').replace(',', '.')
    # Encontrar la posición del último punto
    ultimo_punto = precio.rfind('.')
    if ultimo_punto != -1:
        # Reemplazar todos los puntos excepto el último
        # se parte en dos cadenas usando el punto decimal, se eliminan los que no sean puntos
        # de separacion decimales y se concatenan las cadenas por el punto decimal
        precio = precio[:ultimo_punto].replace('.', '') + precio[ultimo_punto:]
    # Convertir la cadena a float
    return float(precio)

# Funcion para tratar y formatear el texto extraido de marca
def formateo_marca(text):
    # Encuentra la posición del último guion
    ultimo_guion = text.rfind('-')
    # Extrae la marca que está después del último guion y quita espacios
    marca = text[ultimo_guion + 1:].strip()
    return marca

# Conexion a MongoDB y creacion de coleccion
cliente = MongoClient('mongodb://localhost:27017')
db = cliente['Materiales_odontologia']
coleccion = db['Henry_schein']

# objeto options donde definiremos user agent y headlees mode para operar sin abrir el navegador
options = Options()
#options.add_argument("--headless")

# configurar el driver para que Selenium busque e instale el driver correspondiente
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# Abrir la pagina web
driver.get('https://www.henryschein.es/es-es/dentalclinica/c/browsesupplies')
time.sleep(3)
# lista de los links de las categorias de la pagina
categorias = driver.find_elements(By.XPATH, '//ul[@class="hs-categories display grid clear-fix"]/li[@class="item"]/a')

# Extraer los enlaces de cada categoria
links_categorias = [categoria.get_attribute("href") for categoria in categorias]

# iterar sobre categorias
for url_categoria in links_categorias:
    try:
        # ir al link de la categoria
        driver.get(url_categoria)
        print(f"entrando en categoria {url_categoria}")
        # esperar a que cargue la pagina
        time.sleep(3)
        # obtener los link de las subcategorias
        subcategorias = driver.find_elements(By.XPATH,
                                             '//ul[@class="hs-categories display grid clear-fix"]/li[@class="item"]/a')
        # extraer los links de las subcategorias
        links_subcategorias = [subcategoria.get_attribute("href") for subcategoria in subcategorias]
        # iterar sobre las subcategorias
        for url_subcat in links_subcategorias:
            try:
                # ir a link de subcategoria
                driver.get(url_subcat)
                print(f"entrando en subcategoria {url_subcat}")
                # esperar a que cargue la pagina
                time.sleep(3)
                # manejando paginacion
                pagina_actual = 1
                while True:
                    print(f"procesando pagina {pagina_actual}")
                    # obtener los link de producto
                    productos = driver.find_elements(By.XPATH, '//h2[@class="product-name"]/a')
                    # extraer los enlaces de productos
                    links_productos = [producto.get_attribute("href") for producto in productos]
                    # iterar sobre productos
                    for url_producto in links_productos:
                        try:
                            # ir a detalle de producto
                            driver.get(url_producto)
                            print(f"entrando en producto {url_producto}")
                            # esperar a que cargue la pagina
                            time.sleep(4)
                            # Extraer la informacion
                            nombre = driver.find_element(By.XPATH, "//h2[@class='product-title medium strong']").text
                            categoria = driver.find_element(By.XPATH,
                                                            "//div[@class='breadcrumb  no-featured-offers']//li[5]//span").text
                            subcategoria = driver.find_element(By.XPATH,
                                                               "//div[@class='breadcrumb  no-featured-offers']//li[7]//span").text
                            marca = driver.find_element(By.XPATH, '//div[@class="breadcrumb  no-featured-offers"]//ol//li[9]/span').text
                            precio = driver.find_element(By.XPATH, "//span[@class='amount x-small']").text
                            url = driver.find_element(By.XPATH, "//meta[@itemprop='item']").get_attribute("content")

                            # tratar la variable marca para extraer solo la marca de esa cadena de texto con funcion
                            # formateo_marca()
                            formateo_marca(marca)

                            # Convertir y formatear precio con funcion convertir_precio()
                            convertir_precio(precio)
                            print(f"extraccion de {nombre,categoria,subcategoria,marca,precio,url} correcta")
                            # Creo un diccionario item para guardar la informacion y tranferirla luego a la coleccion
                            # de MongoDb
                            item = {
                                "nombre": nombre,
                                "categoria": categoria,
                                "subcategoria": subcategoria,
                                "marca": formateo_marca(marca),
                                "precio": convertir_precio(precio),
                                "url": url
                            }
                            # Insertar/Actualizar el item en la colección de MongoDB
                            guardado = coleccion.update_one({"url": url}, {"$set": item}, upsert=True)
                            # Usando .upserted_id nos devolvera None si no existe update y el id si existe update
                            # si devuelve id hay update y el mensaje sera de actualización sino será de inserción
                            if guardado.upserted_id is not None:
                                print(f"Insercion de {item} en {coleccion} de MongoDb correcta")
                            else:
                                print(f"Actualizacion de {item} en {coleccion} de MongoDb correcta")

                        except NoSuchElementException as e:
                            print(f"Excepcion en extraccion de {url_producto}")
                            print(e.stacktrace)
                            print(f"posible cambio en xpath de precio")
                            # En caso de no encontrar el elemento precio porque este de oferta y se  modifice la ruta
                            # del xpath extraer usando ruta modificada
                            nombre = driver.find_element(By.XPATH, "//h2[@class='product-title medium strong']").text
                            categoria = driver.find_element(By.XPATH,
                                                            "//div[@class='breadcrumb  no-featured-offers']//li[5]//span").text
                            subcategoria = driver.find_element(By.XPATH,
                                                               "//div[@class='breadcrumb  no-featured-offers']//li[7]//span").text
                            marca = driver.find_element(By.XPATH,
                                                        '//div[@class="breadcrumb  no-featured-offers"]//ol//li[9]/span').text
                            precio = driver.find_element(By.XPATH, "//span[@class='large color-quaternary custom-style-price']").text
                            url = driver.find_element(By.XPATH, "//meta[@itemprop='item']").get_attribute("content")

                            # tratar datos extraidos con sus funciones

                            formateo_marca(marca)
                            convertir_precio(precio)

                            # Creo un diccionario item para guardar la informacion y tranferirla luego a la coleccion
                            # de MongoDb
                            item = {
                                "nombre": nombre,
                                "categoria": categoria,
                                "subcategoria": subcategoria,
                                "marca": formateo_marca(marca),
                                "precio": convertir_precio(precio),
                                "url": url
                            }
                            # Insertar/Actualizar el item en la colección de MongoDB
                            guardado = coleccion.update_one({"url": url}, {"$set": item}, upsert=True)
                            if guardado.upserted_id is not None:
                                print(f"Insercion de {item} en {coleccion} de MongoDb correcta")
                            else:
                                print(f"Actualizacion de {item} en {coleccion} de MongoDb correcta")



                    # Ver si existe una siguiente pagina para la paginacion
                    next_page = driver.find_elements(By.XPATH, "//a[@class='hs-paging-next']")
                    if next_page:
                        # si hay next page pulsar
                        next_page[0].click()
                        # aumentar el contador de pagina
                        pagina_actual += 1
                        # esperar a que cargue
                        time.sleep(3)
                    else:
                        break

                # Retroceder hacia el inicio (3 veces por cada profundidad de paginacion)
                driver.back()
                driver.back()
                driver.back()
            except NoSuchElementException as e:
                print(f"Error extraer subcategoria {url_subcat}")
    except NoSuchElementException as e:
        print(f"Error al extraer categoria {url_categoria}")
# cerrar navegador
driver.quit()
