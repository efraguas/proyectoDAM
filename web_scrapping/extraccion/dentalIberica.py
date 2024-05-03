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
coleccion = db['Dental_Iberica']


class Producto(Item):
    nombre = Field()
    categoria = Field()
    subcategoria = Field()
    marca = Field()
    url = Field()
    precio = Field()


class WebIberica(CrawlSpider):
    name = 'dentaliberica'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/113.0.0.0 Safari/537.36',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'CLOSESPIDER_PAGECOUNT': 1063
    }
    allowed_domains = ['dentaliberica.com/es/clinica']

    start_urls = ['https://dentaliberica.com/es/clinica']

    rules = (
        Rule(
            LinkExtractor(
                allow=r'page=\d+$'
            ), follow=True
        ),
        Rule(
            LinkExtractor(
                allow=r'/.html$'
            ), follow=True, callback='parse_iberica'
        )


    )

    def parse_iberica(self, response):
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


with open('./datos/productos_dentalIberica.json') as archivo:
    datos = json.load(archivo)

coleccion.insert_many(datos)
print("coleccion añadida correctamente")


#Ejecucion
proceso = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI': './datos/productos_dentalIberica.json'
})
proceso.crawl(WebIberica)
proceso.start()