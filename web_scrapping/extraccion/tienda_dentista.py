import json
from pymongo import MongoClient
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose
from scrapy.crawler import CrawlerProcess


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


class TiendaDentista(CrawlSpider):
    name = 'latiendadeldentista'
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8'
    }
    allowed_domains = ['latiendadeldentista.com/13-instrumental-dental',
                       'latiendadeldentista.com/343-materiales-dentales', 'latiendadeldentista.com/15-ortodoncia',
                       'latiendadeldentista.com/195-ropa']
    start_urls = [
        'https://www.latiendadeldentista.com/13-instrumental-dental']
    download_delay = 1

    rules = (
        # paginacion horizontal a traves de la lista de categorias
        Rule(
            LinkExtractor(
                allow=r'page=\d+$ | p=\d+$',
                restrict_xpaths="//div[@id='center_column']/ul[@class='product_list row list']"
            ), follow=True),
        # detalle del producto aqui es donde realizamos la extraccion (callback)
        Rule(
            LinkExtractor(
                allow=r'\d{5}$',
                restrict_xpaths="//div[@class='row']"
            ), follow=True, callback='parse_dentista'),
    )

    # Funcion formatear datos extraidos:
    def formatear(self, texto):
        format = texto.replace('\n', '').replace('\t', '').lower().strip()
        return format

    # Funcion formatear el precio y castearlo a float
    def format_precio(self, texto):
        try:
            precio = texto.replace('\n', '').replace('\t', '').replace(" €", '').replace(",", '.').strip()
            float(precio)
        except Exception:
            precio = 'Precio no diponible'
        return precio


    def parse_dentista(self, response):

        selector = Selector(response).get()
        item = ItemLoader(Producto(), selector)

        try:
            item.add_xpath('nombre', ".//h1[@itemprop='name']/text()", MapCompose(self.formatear))
            item.add_xpath('categoria', ".//span[@class='navigation_page']/*[1]//span[@itemprop='title']/text()",
                           MapCompose(self.formatear))
            item.add_xpath('subcategoria',
                           ".//span[@class='navigation_page']/*[3]//span[@itemprop='title']/text()",
                           MapCompose(self.formatear))
            item.add_xpath('marca', ".//p[@id='product_manufacturer']//a/text()", MapCompose(self.formatear))
            item.add_xpath('url', ".//p[@class='our_price_display']//meta[@itemprop='url']/@content",
                           MapCompose(self.formatear))
            item.add_xpath('precio', ".//span[@id='our_price_display']/text()", MapCompose(self.format_precio))

        except:
            pass

        yield item.load_item()



#Ejecucion
proceso = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI': './datos/tiendaDentista.json'
})
proceso.crawl(TiendaDentista)
proceso.start()


#with open('./datos/tiendaDentista.json') as archivo:
#    datos = json.load(archivo)

#coleccion.insert_many(datos)
#print("coleccion añadida correctamente")

#Ejecucuion desde la terminal
#scrapy runspider tienda_dentista.py -o productos_dentales.json