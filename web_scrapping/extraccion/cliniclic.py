from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from pymongo import MongoClient


#Conexion a MongoDB y creacion de coleccion
cliente = MongoClient('mongodb://localhost:27017')
db = cliente['Materiales_odontologia']
coleccion = db['cliniclic']


class Producto(Item):
    nombre = Field()
    categoria = Field()
    subcategoria = Field()
    marca = Field()
    url = Field()
    precio = Field()

class WebCliniClic(CrawlSpider):
    name = 'cliniCic'
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
        'ITEM PIPELINES': {
            'cliniclic.MongoDBPipeline': 300,
        }
    }
    allowed_domains = ['cliniclic.com']
    start_urls = ['https://cliniclic.com/catalogo-productos-dentales']

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/categorias/[a-zA-Z0-9-]+$'
            ), follow=True
        ),
        Rule(
            LinkExtractor(
                allow=r'page=\d+$'
            ), follow=True, callback='extraer_categoria'
        ),
        Rule(
            LinkExtractor(
                allow=r'/position=\d+$'
            ), callback='parse_cliniclic'
        )

    )

    def parse_cliniclic(self, response):
        item = {}
        item['nombre'] = response.xpath("//div[@class='c-product-detail__title-ref ng-tns-c110-8487']/h1/text()").get()
        item['categoria'] = self.extraer_categoria(response)
        item['subcategoria'] = response.xpath("//div[@class='product-view']@data-subfamily").get()
        item['marca'] = response.xpath("//li[@class='c-product-detail__dist-maker-item maker ng-tns-c110-8487']/a/text()").get()
        item['url'] = response.xpath("//link[@rel='canonical']/@href").get()
        precio = response.xpath("//h2[@id='priceProduct']/text()").get()
        item['precio'] = float(precio.replace('€', '').replace(",", '.').rstrip('.0')) if precio else 'Precio no disponible'
        yield item

    def extraer_categoria(self, response):
        # extraer categoria y subcategoria
        categoria = response.xpath("//li[@class='c-breadcrumb-module__item ng-star-inserted']/a/text()").get()
        return categoria

# Pipeline para guardar datos extraidos en coleccion de MongoDB
class MongoDBPipeline:
    def __init__(self):
        self.cliente = MongoClient('localhost', 27017)
        self.db = self.cliente['Materiales_odontologia']
        self.collection = self.db['ClinicClic']

# Metodo para efectuar el guardado y actualizacion de valores
    def process_item(self, item, spider):
        self.collection.update_one({'url': item['url']}, {'$set': dict(item)}, upsert=True)
        return item


#configuracion y ejecucion
if __name__ == "__main__":
    custom_settings = {
        'ITEM_PIPELINES': {
            'cliniclic.MongoDBPipeline': 300,
        }
    }
    # Ejecucion
    proceso = CrawlerProcess(settings=custom_settings)
    proceso.crawl(WebCliniClic)
    proceso.start()