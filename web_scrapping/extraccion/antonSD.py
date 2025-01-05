from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from pymongo import MongoClient




class Producto(Item):
    nombre = Field()
    categoria = Field()
    subcategoria = Field()
    marca = Field()
    imagen = Field()
    url = Field()
    precio = Field()


# Spider que recorre las urls y  para extraer la información
class WebAntonSD(CrawlSpider):
    name = 'antonSD'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/113.0.0.0 Safari/537.36',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DOWNLOADER_MIDDLEWARES': {'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610,
                                   'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,},
        'ZYTE_SMARTPROXY_ENABLED': True,
        'ZYTE_SMARTPROXY_API_KEY': '23ef2fc5c6e54e71a06b47e92ca203db',
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

    # metodo extractor de la informacion
    def parse_antonSD(self, response):
        item = {}
        item['nombre'] = response.xpath(".//div[@class='shop-product-info']//h1/text()").get()
        item['categoria'] = response.xpath(".//p[@class='breadcrumb']//a[3]/text()").get()
        subcategoria = response.xpath("//p[@class='breadcrumb']//a[4]/text()").get()
        item['subcategoria'] = subcategoria
        marca= response.xpath(".//div[@class='shop-product-info']//h3/text()").get()
        item['marca'] = marca if marca else 'sin marca'
        item['imagen'] = response.xpath(".//div[@class='shop-product-images']//img/@src").get()
        item['url'] = response.xpath(".//meta[@property='og:url']/@content").get()
        precio = response.xpath(".//ul[@class='shop-product-precios']//span/text()|ul[@class='shop-product-precios']//input[@id='offer_price']/@value").get()
        item['precio'] = float(precio.replace('€', '').replace(",", '.').rstrip('.0')) if precio else 'Precio no disponible'

        yield item


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
