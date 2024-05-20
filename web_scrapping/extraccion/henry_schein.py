import time

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#Conexion a MongoDB y creacion de coleccion
cliente = MongoClient('mongodb://localhost:27017')
db = cliente['Materiales_odontologia']
coleccion = db['Henry_schein']

# objeto options donde definiremos usera agent y headlees mode para operar sin abrir el navegador
options = Options()
options.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/113.0.0.0 Safari/537.36'")
options.add_argument("--headless")

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
        # esperar a que cargue la pagina
        time.sleep(3)
        # obtener los link de las subcategorias
        subcategorias = driver.find_elements(By.XPATH, '//ul[@class="hs-categories display grid clear-fix"]/li[@class="item"]/a')
        # extraer los links de las subcategorias
        links_subcategorias = [subcategoria.get_attribute("href") for subcategoria in subcategorias]
        # iterar sobre las subcategorias
        for url_subcat in links_subcategorias:
            try:
                # ir a link de subcategoria
                driver.get(url_subcat)
                # esperar a que cargue la pagina
                time.sleep(3)
                #manejando paginacion
                pagina_actual = 1
                while True:
                    # obtener los link de producto
                    productos = driver.find_elements(By.XPATH, '//ul[@class="hs-categories display grid clear-fix"]/li[@class="item"]/a')
                    # extraer los enlaces de productos
                    links_productos = [producto.get_attribute("href") for producto in productos]
                    # iterar sobre productos
                    for url_producto in links_productos:
                        try:
                            # ir a detalle de producto
                            driver.get(url_producto)
                            # esperar a que cargue la pagina
                            time.sleep(3)
                            # Extraer la informacion
                            nombre = driver.find_element(By.XPATH, "//h2[@class='product-title medium strong'].text")
                            categoria = driver.find_element(By.XPATH, "//div[@class='breadcrumb  no-featured-offers']//li[5]//span.text")
                            subcategoria = driver.find_element(By.XPATH, "//div[@class='breadcrumb  no-featured-offers']//li[7]//span.text")
                            marca = driver.find_element(By.XPATH, '//title.text')
                            precio = driver.find_element(By.XPATH, "//span[@class='amount x-small'].text")
                            url = driver.find_element(By.XPATH, "//meta[@itemprop='item']/@content").get_attribute("content")

                            #tratar la variable marca para extraer solo la marca de esa cadena de texto
                            marca_formateada = marca.split()
                            marca = marca_formateada[-6]

                            # eliminar simbolo de euro del texto precio
                            float(precio.replace('€', '').replace(",", '.').rstrip(
                                '.0')) if precio else 'Precio no disponible'

                            # Creo un diccionario item para guardar la informacion y tranferirla luego a la coleccion
                            # de MongoDb
                            item = {
                                "nombre": nombre,
                                "categoria" : categoria,
                                "subcategoria" : subcategoria,
                                "marca" : marca,
                                "precio" : precio,
                                "url" : url
                            }
                            # Insertar el item en la colección de MongoDB
                            coleccion.insert_one(item)

                        except Exception as e:
                            print(f"Excepcion en extraccion de {url_producto}")

                    # Ver si existe una siguiente pagina para la paginacion
                    next_page = driver.find_element(By.XPATH, "//a[class='hs-paging-next']")
                    if next_page:
                        # si hay next page pulsar
                        next_page[0].click()
                        #aumentar el contador de pagina
                        pagina_actual += 1
                        # esperar a que cargue
                        time.sleep(3)
                    else:
                        break

                # Retroceder hacia el inicio (3 veces por cada profundidad de paginacion)
                driver.back()
                driver.back()
                driver.back()
            except Exception as e:
                print(f"Error extraer subcategoria {url_subcat}")
    except Exception as e:
        print(f"Error al extraer categoria {url_categoria}")
# cerrar navegador
driver.quit()