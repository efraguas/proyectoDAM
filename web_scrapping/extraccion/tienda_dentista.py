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
    allowed_domains = ['latiendadeldentista.com']
    start_urls = ['https://www.latiendadeldentista.com/13-instrumental-dental']
    #download_delay = 1

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

    # Funcion formatear datos extraidos:
    def formatear(self, texto):
        return texto.replace('\n', '').replace('\t', '').lower().strip()

    # Funcion formatear el precio y castearlo a float
    def format_precio(self, texto):
        try:
            precio = texto.replace('\n', '').replace('\t', '').replace(" €", '').replace(",", '.').strip()
            return float(precio)
        except ValueError:
            return 'Precio no diponible'

    def parse_dentista(self, response):
        item = ItemLoader(item=Producto(), response=response)
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
        },
        'FEEDS': {
            './datos/productos_dentalIberica.json': {
                'format': 'json',
                'overwrite': True,
            }
        }
    }
    proceso = CrawlerProcess(settings=custom_settings)
    proceso.crawl(TiendaDentista)
    proceso.start()

#Ejecucuion desde la terminal
#scrapy runspider tienda_dentista.py -o productos_dentales.json para especificar guardado en archivo json
#scrapy runspider tienda_dentista.py para usar el pipeline y guardar en MongoDB

