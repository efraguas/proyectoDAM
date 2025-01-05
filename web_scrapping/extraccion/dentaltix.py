from pymongo import MongoClient
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


# Spider que recorre las urls y  para extraer la información
class Dentaltix(CrawlSpider):
    name = 'dentaltix'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/113.0.0.0 Safari/537.36',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DOWNLOADER_MIDDLEWARES': {'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610,
                                   'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,},
        'ZYTE_SMARTPROXY_ENABLED': True,
        'ZYTE_SMARTPROXY_API_KEY': '23ef2fc5c6e54e71a06b47e92ca203db',
        'ITEM PIPELINES': {
            'dentaltix.MongoDBPipeline': 300,
        }
    }

    start_urls = ["https://www.dentaltix.com/es/mapa-del-sitio"]
    allowed_domains = ["dentaltix.com"]

    rules = (

        Rule(
            LinkExtractor(
                restrict_xpaths= "//div[@class='field field-name-body field-type-text-with-summary field-label-hidden']//ul/li/a",

            ), follow=True,
        ),

        Rule(
            LinkExtractor(
                restrict_xpaths="//div[@id='products-display-page']//a[@class='product-item-title']",
            ),callback='parse_products',follow=True,
        )
    )

    def parse_products(self, response):
        precio_int = response.xpath("//span[@class='base-price-int']/text()").get(default="0")
        precio_float = response.xpath("//span[@class='base-price-dec']/text()").get(default="00")
        precio = float(f"{precio_int}.{precio_float}")

        item = {}
        item['nombre'] = response.xpath(".//div[@class='title-price']//h1/text()").get().strip()
        item['categoria'] = response.xpath(".//div[@id='breadcrumbs']//a[3]/text()").get().strip()
        item['subcategoria'] = response.xpath(".//div[@id='breadcrumbs']//a[4]/text()").get().strip()
        marca = response.xpath(".//div[@class='title-price']//div[2]/a/text()").get()
        item['marca'] = marca if marca else 'sin marca'
        item['imagen'] = response.xpath(".//div[@class='product-main-image']/img/@src").get()
        item['url'] = response.xpath(".//link[@rel='canonical']/@href").get()
        item['precio'] = precio if precio is not None else 'Precio no disponible'

        yield item

# Pipeline para guardar datos extraidos en coleccion de MongoDB
class MongoDBPipeline:


    def __init__(self):
        self.cliente = MongoClient('localhost', 27017)
        self.db = self.cliente['Materiales_odontologia']
        self.collection = self.db['Productos']

    # Metodo para efectuar el guardado y actualizacion de valores
    def process_item(self, item, spider):
        self.collection.update_one({'url': item['url']}, {'$set': dict(item)}, upsert=True)
        return item


#configuracion y ejecucion
if __name__ == "__main__":
    custom_settings = {
        'ITEM_PIPELINES': {
            'dentaltix.MongoDBPipeline': 300,
        }
    }
    # Ejecucion
    proceso = CrawlerProcess(settings=custom_settings)
    proceso.crawl(Dentaltix)
    proceso.start()
