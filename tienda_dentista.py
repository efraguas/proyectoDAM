from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose
from scrapy.crawler import CrawlerProcess


class Producto(Item):
    """
    defino la clase producto con los atributos de la informacion que deseo extraer en este caso
        nombre
        categoria
        subcategoria
        marca
        url
        precio
    """
    nombre = Field()
    categoria = Field()
    subcategoria = Field()
    marca = Field()
    url = Field()
    precio = Field()


class TiendaDentista(CrawlSpider):
    """
    Clase que define el spider a utilizar sobre la web latiendadeldentista para la extraccion de la informacion acerca
    de los materiales odontológicos y las reglas para la paginacion horizontal y vertical de la url
    """
    name = 'latiendadeldentista'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/113.0.0.0 Safari/537.36',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }
    allowed_domains = ['latiendadeldentista.com']
    start_urls = [
        'https://www.latiendadeldentista.com',

    ]
    download_delay = 1

    rules = (
        # Detalle de categorias
        # paginacion horizontal a traves de la lista de categorias
        Rule(
            LinkExtractor(
                allow=r'\b(?!(11|21|304|420|295))\d+-\w+\b',
                restrict_xpaths="//div[@class='subcategory-image']/a"
            ), follow=True),
        # detalle de subcategorias
        # paginacion vertical a través de la lista de subcategorias
        Rule(
            LinkExtractor(
                allow=r'\d+-\w+',
                restrict_xpaths="//div[@class='subcategory-image']/a"
            ), follow=True),
        #
        # paginacion vertical a traves de los productos de las subcategorias
        Rule(
            LinkExtractor(
                allow=r'\d+-\w+'
            ), follow=True),
        # detalle del producto aqui es donde realizamos la extraccion (callback)
        Rule(
            LinkExtractor(
                allow=r'\d+\w+',
                restrict_xpaths="//div[@class='columns-container']//a[@class='product_img_link']"
            ), follow=True, callback='parse_web'),
    )


    def parse_web(self, response):
        """
        nombre = selector.xpath("//h1[@itemprop='name']/text()").get()
        categoria = selector.xpath("//span[@class='navigation_page']/*[1]//span[@itemprop='title']/text()").get()
        subcategoria = selector.xpath("//span[@class='navigation_page']/*[3]//span[@itemprop='title']/text()").get()
        marca = selector.xpath("//p[@id='product_manufacturer']//a/text()").get()
        url = selector.xpath("//p[@class='our_price_display']//meta[@itemprop='url']/@content").get()
        """
        selector = Selector(response).get()
        precio = selector.xpath("//span[@class='our_price_display']").get()
        float(precio.replace('\t', '').replace(" €+IVA", '').replace(",", '.'))

        item = ItemLoader(Producto(), selector)
        try:

            item.add_xpath('nombre', ".//h1[@itemprop='name']/text()"), MapCompose(
                lambda x: x.replace('\n', '').replace('\t', '').replace(" €+IVA", ''))
            item.add_xpath('categoria',
                           ".//span[@class='navigation_page']/*[1]//span[@itemprop='title']/text()"), MapCompose(
                lambda x: x.replace('\n', '').replace('\t', '').replace(" €+IVA", ''))
            item.add_xpath('subcategoria',
                           ".//span[@class='navigation_page']/*[3]//span[@itemprop='title']/text()"), MapCompose(
                lambda x: x.replace('\n', '').replace('\t', '').replace(" €+IVA", ''))
            item.add_xpath('marca', ".//p[@id='product_manufacturer']//a/text()"), MapCompose(
                lambda x: x.replace('\n', '').replace('\t', '').replace(" €+IVA", ''))
            item.add_xpath('url', ".//p[@class='our_price_display']//meta[@itemprop='url']/@content"), MapCompose(
                lambda x: x.replace('\n', '').replace('\t', '').replace(" €+IVA", ''))
            item.add_value('precio', precio)
        except:
            pass

        yield item.load_item()

#Ejecucion
proceso = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI': 'productos_dentales.json'
})
proceso.crawl(TiendaDentista)
proceso.start()

#Ejecucuion desde la terminal
#scrapy runspider tienda_dentista.py -o productos_dentales.json