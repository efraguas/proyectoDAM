from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from pymongo import MongoClient

# Conexion a MongoDB y creacion de coleccion
cliente = MongoClient('mongodb://localhost:27017')
db = cliente['Materiales_odontologia']
coleccion = db['Dental_Iberica']


class Producto(Item):
    nombre = Field()
    categoria = Field()
    subcategoria = Field()
    marca = Field()
    url = Field()
    precio = Field()


# Spider extractor de datos
class WebIberica(CrawlSpider):
    name = 'dentaliberica'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.119 Safari/537.36',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'CLOSESPIDER_PAGECOUNT': 1063,
        'ITEM PIPELINES': {
            'dentalIberica.MongoDBPipeline': 300,
        }
    }

    start_urls = ['https://dentaliberica.com/es/clinica']

    rules = (
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
        item['url'] = response.xpath(".//meta[@property='og:url']/@content").get()
        item['precio'] = response.xpath(".//meta[@property='product:price:amount']/@content").get()

        yield item

# Pipeline para guardar datos extraidos en coleccion de MongoDB
class MongoDBPipeline:
    def __init__(self):
        self.cliente = MongoClient('localhost', 27017)
        self.db = self.cliente['Materiales_odontologia']
        self.collection = self.db['dental_Iberica']

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
