from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose
from scrapy.crawler import CrawlerProcess
from pymongo import MongoClient
import json


#Conexion a MongoDB y creacion de coleccion
cliente = MongoClient('mongodb://localhost:27017')
db = cliente['Materiales_odontologia']
coleccion = db['LaTiendaDentista']


class Producto(Item):
    """
    defino la clase producto con los atributos de la informacion que deseo extraer en este caso
        nombre
        categoria
        subcategoria
        marca
        url
        precio
    """
    nombre = Field()
    categoria = Field()
    subcategoria = Field()
    marca = Field()
    url = Field()
    precio = Field()


class WebDentista(CrawlSpider):
    """
    Clase que define el spider a utilizar sobre la web latiendadeldentista para la extraccion de la informacion acerca
    de los materiales odontológicos y las reglas para la paginacion horizontal y vertical de la url
    """
    name = 'latiendadeldentista'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/113.0.0.0 Safari/537.36',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }
    allowed_domains = ['latiendadeldentista.com',
                       ]
    start_urls = [
        'https://www.latiendadeldentista.com'
        ]

    rules = (
        Rule(
            LinkExtractor(
                allow=r'\d+-ropa|\d+-ortodoncia|\d+-instrumental-dental|\d+-materiales-dentales'
            ), follow=True
        ),

        # paginacion horizontal a traves de los productos de cada seccion
        Rule(
            LinkExtractor(
                allow=r'p\d+|page-\d+',
                restrict_xpaths="//ul[@class='product_list row list']"
            ), follow=True
        ),
        #paginacion vertical al detalle de cada producto
        Rule(
            LinkExtractor(
                allow=r'\d+-',
            ), follow=True, callback='parse_web'
        )
    )

    # Funcion formatear datos extraidos:
    def formatear(self, texto):
        format = texto.replace('\n', '').replace('\t', '').lower().strip()
        return format

    # Funcion formatear el precio y castearlo a float
    def format_precio(self, texto):
        try:
            precio = texto.replace('\n', '').replace('\t', '').replace(" €", '').replace(",", '.').strip()
            float(precio)
        except Exception:
            precio = 'Precio no diponible'
        return precio

    # Método para extraer la información de cada producto
    def parse_web(self, response):
        selector = Selector(response)
        productos = selector.xpath("//div[@class='columns-container']")

        item = ItemLoader(Producto(), productos)

        item.add_xpath('nombre', ".//h1[@itemprop='name']/text()", MapCompose(self.formatear))
        item.add_xpath('categoria', ".//span[@class='navigation_page']/*[1]//span[@itemprop='title']/text()",
                       MapCompose(self.formatear))
        item.add_xpath('subcategoria',
                       ".//span[@class='navigation_page']/*[3]//span[@itemprop='title']/text()",
                       MapCompose(self.formatear))
        item.add_xpath('marca', ".//p[@id='product_manufacturer']//a/text()", MapCompose(self.formatear))
        item.add_xpath('url', ".//p[@class='our_price_display']//meta[@itemprop='url']/@content",
                       MapCompose(self.formatear))
        item.add_xpath('precio', ".//span[@id='our_price_display']/text()", MapCompose(self.format_precio))

        yield item.load_item()



# Ejecucion del script
proceso = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI': './datos/productos_dentales.json'
})
proceso.crawl(WebDentista)
proceso.start()

#Acceso al archivo json e insercion en la coleccion de la base de datos
with open('./datos/tiendaDentista.json') as archivo:
    datos = json.load(archivo)
coleccion.insert_many(datos)
print("datos añadidos correctamente")


# Ejecucuion desde la terminal
# scrapy runspider tienda_dentista.py -o productos_dentales.json
