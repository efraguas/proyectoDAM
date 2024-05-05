from pymongo import MongoClient
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose
from scrapy.crawler import CrawlerProcess

#Conexion a MongoDB y creacion de coleccion
cliente = MongoClient('mongodb://localhost:27017')
db = cliente['Materiales_odontologia']
coleccion = db['tienda_dentista']

class Producto(Item):
    nombre = Field()
    categoria = Field()
    subcategoria = Field()
    marca = Field()
    url = Field()
    precio = Field()


class TiendaDentista(CrawlSpider):
    name = 'latiendadeldentista'
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
        'ITEM_PIPELINES': {
            'tienda_dentista.MongoDBPipeline': 300,
        },
    }

    start_urls = ['https://www.latiendadeldentista.com', 'https://latiendadeldentista.com/343-materiales-dentales',
                  'https://latiendadeldentista.com/195-ropa']

    rules = (
        # paginacion horizontal a traves de la lista de categorias
        Rule(
            LinkExtractor(
                allow=r'\d+$',
                restrict_xpaths="//div[@class='row']"
            ), callback='parse_dentista'),
        Rule(
            LinkExtractor(
                allow=r'page=\d+$|p=\d+$',
                restrict_xpaths="//div[@id='center_column']/ul[@class='product_list row list']"
            ),
            # detalle del producto aqui es donde realizamos la extraccion (callback)
        )
    )


    def parse_dentista(self, response):
        item = {}
        nombre = response.xpath(".//h1[@itemprop='name']/text()").get()
        item['nombre'] = formatear(nombre)
        categoria = response.xpath(".//span[@class='navigation_page']/*[1]//span[@itemprop='title']/text()").get()
        item['categoria'] = formatear(categoria)
        subcategoria = response.xpath(".//span[@class='navigation_page']/*[3]//span[@itemprop='title']/text()").get()
        item['subcategoria'] = formatear(subcategoria)
        marca = response.xpath( ".//p[@id='product_manufacturer']//a/text()").get()
        item['marca'] = formatear(marca)
        url = response.xpath(".//p[@class='our_price_display']//meta[@itemprop='url']/@content").get()
        item['url'] = formatear(url)
        precio = response.xpath(".//span[@id='our_price_display']/text()").get()
        item['precio'] = format_precio(precio) if precio else 'no disponible'

        yield item


# Funcion formatear datos extraidos:
def formatear(texto):
    if texto:
        return texto.replace('\n', '').replace('\t', '').lower().strip()
    else:
        return 'no disponible'

# Funcion formatear el precio
def format_precio( texto):
    try:
        precio = texto.replace('\n', '').replace('\t', '').replace(" €", '').replace(",", '.').rstrip('.0').strip()
        return float(precio)
    except ValueError:
        return 'Precio no diponible'



# Pipeline para MongoDB
class MongoDBPipeline:
    def __init__(self):
        self.cliente = MongoClient('localhost', 27017)
        self.db = self.cliente['Materiales_odontologia']
        self.collection = self.db['tienda_dentista']

    def process_item(self, item, spider):
        self.collection.update_one({'url': item['url']}, {'$set': dict(item)}, upsert=True)
        return item


# Configuración y ejecución
if __name__ == "__main__":
    custom_settings = {
        'ITEM_PIPELINES': {
            'tiendaDentista.MongoDBPipeline': 300,
        }
    }
    proceso = CrawlerProcess(settings=custom_settings)
    proceso.crawl(TiendaDentista)
    proceso.start()

#Ejecucuion desde la terminal
#scrapy runspider tienda_dentista.py -o productos_dentales.json para especificar guardado en archivo json
#scrapy runspider tienda_dentista.py para usar el pipeline y guardar en MongoDB

