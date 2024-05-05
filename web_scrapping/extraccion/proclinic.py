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
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/113.0.0.0 Safari/537.36',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'ITEM PIPELINES': {
            'proclinic.MongoDBPipeline': 300,
        }
    }
    allowed_domains = ['proclinic.es/tienda/']

    start_urls = ['https://www.proclinic.es/tienda/clinica.html?p=1&limit=24&orderBy[name]=asc&filters['
                  'main_family]=Cl%C3%ADnica'
                  ]

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/([\w-]+(?:-[\w-]+)*)\/?|/.html$'
            ), callback='parse_proclinic'
        )
    )

    def parse_proclinic(self, response):
        selector = Selector(response)
        productos = selector.xpath("")

        item = ItemLoader(Producto(), productos)
        item.add_xpath('nombre', '')
        item.add_xpath('categoria', '')
        item.add_xpath('subcategoria', '')
        item.add_xpath('marca', '')
        item.add_xpath('url', '')
        item.add_xpath('precio', '')

        yield item.load_item()


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




