from itemloaders.processors import MapCompose
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
from pymongo import MongoClient

#Conexion a MongoDB y creacion de coleccion
cliente = MongoClient('mongodb://localhost:27017')
db = cliente['Materiales_odontologia']
coleccion = db['Anton_SD']


class Producto(Item):
    nombre = Field()
    categoria = Field()
    subcategoria = Field()
    marca = Field()
    url = Field()
    precio = Field()


# Spider que recorre las urls y  para extraer la información
class WebAntonSD(CrawlSpider):
    name = 'antonSD'
    custom_settings = {
        #'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) '
        #             'Chrome/113.0.0.0 Safari/537.36',
        'FEED_EXPORT_ENCODING': 'utf-8',
        #'CLOSESPIDER_PAGECOUNT': 100,
        'ITEM PIPELINES': {
            'antonSD.MongoDBPipeline': 300,
        }
    }

    start_urls = ['https://www.antonsl.es/consumibles']

    rules = (
        # Regla de paginación para extracción del detalle del producto
        Rule(
            LinkExtractor(
                allow=r'-\d+$|[a-z]$'
            ), callback='parse_antonSD'
        ),
        # Regla de paginación horizontal a traves de las paginas de la url
        Rule(
            LinkExtractor(
                allow=r'page=\d+$'
            )
        )
    )

    # Metodo para formatear el valor del precio extraido a float
    def format_precio(self, texto):
        try:
            return float(texto)
        except ValueError:
            return "No disponible"

    # metodo extractor de la informacion
    def parse_antonSD(self, response):
        item = {}
        item['nombre'] = response.xpath(".//div[@class='shop-product-info']//h1/text()").get()
        item['categoria'] = response.xpath(".//p[@class='breadcrumb']//a[3]/text()").get()
        subcategoria = response.xpath("//p[@class='breadcrumb']//a[4]/text()").get()
        item['subcategoria'] = subcategoria if subcategoria else 'sin subcategoria'
        marca= response.xpath(".//div[@class='shop-product-info']//h3/text()").get()
        item['marca'] = marca if marca else 'sin marca'
        item['url'] = response.xpath(".//meta[@property='og:url']/@content").get()
        precio = response.xpath(".//ul[@class='shop-product-precios']//span/text()").get()
        item['precio'] = float(precio.replace('€', '').replace(",", '.').rstrip('.0')) if precio else 'Precio no disponible'

        yield item
        #
        #
        #
        # selector = Selector(response)
        # productos = selector.xpath("//head | //section[@class='page-header page-header-shop'] | //div[@class='shop-page-content']")
        #
        # item = ItemLoader(item=Producto(), selector=productos)
        # item.add_xpath('nombre', ".//div[@class='shop-product-info']//h1/text()")
        # item.add_xpath('categoria', ".//p[@class='breadcrumb']//a[3]/text()")
        # item.add_xpath('subcategoria', ".//p[@class='breadcrumb']//a[4]/text()")
        # item.add_xpath('url', ".//meta[@property='og:url']/@content")
        # item.add_xpath('precio', ".//ul[@class='shop-product-precios']//input[@id='offer_price']/@value")
        # item.add_xpath('marca', ".//div[@class='shop-product-info']//h3/text()")
        #
        # yield item.load_item()


# Pipeline para guardar datos extraidos en coleccion de MongoDB
class MongoDBPipeline:
    def __init__(self):
        self.cliente = MongoClient('localhost', 27017)
        self.db = self.cliente['Materiales_odontologia']
        self.collection = self.db['antonSD']

    # Metodo para efectuar el guardado y actualizacion de valores
    def process_item(self, item, spider):
        self.collection.update_one({'url': item['url']}, {'$set': dict(item)}, upsert=True)
        return item


#configuracion y ejecucion
if __name__ == "__main__":
    custom_settings = {
        'ITEM_PIPELINES': {
            'antonSD.MongoDBPipeline': 300,
        }
    }
    # Ejecucion
    proceso = CrawlerProcess(settings=custom_settings)
    proceso.crawl(WebAntonSD)
    proceso.start()
