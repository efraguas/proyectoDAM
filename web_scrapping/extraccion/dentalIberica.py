from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from pymongo import MongoClient

# Conexion a MongoDB y creacion de coleccion
cliente = MongoClient('mongodb://localhost:27017')
db = cliente['Materiales_odontologia']
coleccion = db['Productos']


class Producto(Item):
    nombre = Field()
    categoria = Field()
    subcategoria = Field()
    imagen = Field()
    marca = Field()
    url = Field()
    precio = Field()


# Spider extractor de datos
class WebIberica(CrawlSpider):
    name = 'dentaliberica'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6438.69 Safari/537.36',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'COOKIES_ENABLED': True,
        'CLOSESPIDER_PAGECOUNT': 1063,
        'DOWNLOADER_MIDDLEWARES': {'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610},
        'ZYTE_SMARTPROXY_ENABLED': True,
        'ZYTE_SMARTPROXY_API_KEY': '<KEY>',
        'DEFAULT_REQUEST_HEADERS': {
            'Referer': 'https://dentaliberica.com',
            'Accept-Language': 'es',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        },
        'ITEM PIPELINES': {
            'dentalIberica.MongoDBPipeline': 300,
        }
    }

    start_urls = ['https://dentaliberica.com/es']

# Evitar salirse del dominio
    allowed_domains = ['dentaliberica.com']

    rules = (
        Rule(LinkExtractor(allow=(r'/clinica', r'/equipamiento', r'/laboratorio', r'/ofertas', r'/outlet'),
                           deny=r'/content/catálogos-material-odontológico'), follow=True),

        Rule(
            LinkExtractor(
                allow=r'\.html$|\.html#',
            ), callback='parse_iberica'
        ),
        Rule(
            LinkExtractor(
                allow=r'page=\d+$'
            ),
        )

    )

# Clase encargada de parsear la informacion extraida
    def parse_iberica(self, response):
        item = {}
        item['nombre'] = response.xpath(".//meta[@property='og:title']/@content").get()
        item['categoria'] = response.xpath(".//ol/li[3]//span/text()").get()
        item['subcategoria'] = response.xpath(".//ol/li[4]//span/text()").get()
        item['marca'] = response.xpath(".//div[@class='product-manufacturer']//span/text()").get()
        item['imagen'] = response.xpath(".//img[@class='js-qv-product-cover']/@src").get()
        item['url'] = response.xpath(".//meta[@property='og:url']/@content").get()
        precio = response.xpath(".//meta[@property='product:price:amount']/@content").get()
        item['precio'] = float(precio.replace('€', '').replace(",", '.').rstrip('.0')) if precio else 'Precio no disponible'

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
            'dentalIberica.MongoDBPipeline': 300,
        }
    }
    # Ejecucion
    proceso = CrawlerProcess(settings=custom_settings)
    proceso.crawl(WebIberica)
    proceso.start()
