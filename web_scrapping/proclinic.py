
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from pymongo import MongoClient


#Conexion a MongoDB y creacion de coleccion
cliente = MongoClient('mongodb://localhost:27017')
db = cliente['Materiales_odontologia']
coleccion = db['Proclinic']


class Producto(Item):
    nombre = Field()
    categoria = Field()
    subcategoria = Field()
    marca = Field()
    imagen = Field()
    url = Field()
    precio = Field()

class WebProclinic(CrawlSpider):
    name = 'Proclinic'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/113.0.0.0 Safari/537.36',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DOWNLOADER_MIDDLEWARES': {'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610},
        'ZYTE_SMARTPROXY_ENABLED': True,
        'ZYTE_SMARTPROXY_API_KEY': '23ef2fc5c6e54e71a06b47e92ca203db',
        'ITEM PIPELINES': {
            'proclinic.MongoDBPipeline': 300,
        }
    }
    #allowed_domains = ['proclinic.es']
    start_urls = ['https://www.proclinic.es/tienda/clinica.html', 'https://www.proclinic.es/tienda']

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/tienda/.*(-[a-zA-Z0-9]+)*\.html$|.*$'
            ), follow=True, callback='parse_proclinic'
        ),
    )

    def parse_proclinic(self, response):
        item = {}
        item['nombre'] = response.xpath(".//div[@class='product-view product-view--grouped']/@data-name").get()
        item['categoria'] = response.xpath(".//div[@class='product-view product-view--grouped']/@data-category").get()
        item['subcategoria'] = response.xpath(".//div[@class='product-view product-view--grouped']/@data-subfamily").get()
        item['marca'] = response.xpath(".//div[@class='product-view product-view--grouped']/@data-brand").get()
        item['url'] = response.xpath("//meta[@property='og:url']/@content").get()
        item['imagen'] = response.xpath(".//meta[@property='og:image']/@content").get()
        precio = response.xpath(".//div[@class='product-view product-view--grouped']/@data-price").get()
        item['precio'] = float(precio.replace('€', '').replace(",", '.').rstrip('.0')) if precio else 'Precio no disponible'
        yield item


# Pipeline para guardar datos extraidos en coleccion de MongoDB
class MongoDBPipeline:
    def __init__(self):
        mongo_uri = "mongodb+srv://efraguas:<fraguas17>@materiales-odontologia.fkhm2.mongodb.net/?retryWrites=true&w=majority&appName=materiales-odontologia"
        self.cliente = MongoClient(mongo_uri)
        self.db = self.cliente['materiales-odontologia']
        self.collection = self.db['productos_odontologicos']

# Metodo para efectuar el guardado y actualizacion de valores
    def process_item(self, item, spider):
        self.collection.update_one({'url': item['url']}, {'$set': dict(item)}, upsert=True)
        return item


#configuracion y ejecucion
if __name__ == "__main__":
    custom_settings = {
        'ITEM_PIPELINES': {
            'proclinic.MongoDBPipeline': 300,
        }
    }
    # Ejecucion
    proceso = CrawlerProcess(settings=custom_settings)
    proceso.crawl(WebProclinic)
    proceso.start()




