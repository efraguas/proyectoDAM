
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
    url = Field()
    precio = Field()

class WebProclinic(CrawlSpider):
    name = 'Proclinic'
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
        'ITEM PIPELINES': {
            'proclinic.MongoDBPipeline': 300,
        }
    }
    allowed_domains = ['proclinic.es']
    start_urls = ['https://www.proclinic.es/tienda/clinica']

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/tienda/[a-zA-Z0-9-]+'
            ), callback='parse_proclinic'
        )
    )

    def parse_proclinic(self, response):
        item = {}
        item['nombre'] = response.xpath("//div[@class='product-view']@data-name").get()
        item['categoria'] = response.xpath("//div[@class='product-view']@data-category").get()
        item['subcategoria'] = response.xpath("//div[@class='product-view']@data-subfamily").get()
        item['marca'] = response.xpath("//div[@class='product-view']@data-brand").get()
        item['url'] = response.xpath("//div[@class='product-view']@data-thumbnail").get()
        precio = response.xpath("//div[@class='product-view']@data-price").get()
        item['precio'] = float(precio.replace('€', '').replace(",", '.').rstrip('.0')) if precio else 'Precio no disponible'
        yield item


# Pipeline para guardar datos extraidos en coleccion de MongoDB
class MongoDBPipeline:
    def __init__(self):
        self.cliente = MongoClient('localhost', 27017)
        self.db = self.cliente['Materiales_odontologia']
        self.collection = self.db['Proclinic']

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
    proceso.crawl(WebProclinic)
    proceso.start()




