import json
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


class WebAntonSD(CrawlSpider):
    name = 'antonSD'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/113.0.0.0 Safari/537.36',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }
    allowed_domains = ['antonsl.es/consumibles']

    start_urls = ['https://www.antonsl.es/consumibles']

    rules = (
        Rule(
            LinkExtractor(
                allow=r''
            ), follow=True
        ),
        Rule(
            LinkExtractor(
                allow=r''
            ), follow=True, callback='parse_antonSD'
        )


    )

    def parse_antonSD(self, response):
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


with open('./datos/productos_antonSD.json') as archivo:
    datos = json.load(archivo)

coleccion.insert_many(datos)
print("coleccion añadida correctamente")


#Ejecucion
proceso = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI': './datos/productos_antonSD.json'
})
proceso.crawl(WebAntonSD)
proceso.start()