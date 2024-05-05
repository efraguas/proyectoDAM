# proyectoDAM
Proyecto de Desarrollo de Aplicaciones Multiplataforma 

 Este proyecto tiene como objetivo el desarrollo de un programa para la comparación de precios de diferentes materiales enfocado al sector de la odontología, se pretende dar una solución eficiente a dicho sector para la optimización de recursos económicos dando una herramienta que permita a los potenciales usuarios, profesionales de la odontología, comparar productos y materiales de una manera eficiente, ahorro de tiempo, aportando una mejor visión de las opciones disponibles en el mercado y en definitiva facilitar la toma de decisiones. 
 Este programan será desarrollado mediante el uso de la tecnología del web scraping para la extracción de datos relevantes, el uso de base de datos noSql MongoDb y el lenguaje de programación Python. 
 
 Se crean clases extractoras de informacion para cada una de las webs de proveedores de odontoloía de las que se desea extraer 
 información. estas clases han sido construidas usando Scrapy y usando CrawlSpider para crear arañas que paginaran las distintas urls de cada
 web.
 
Por medio del metodo parse, se extrae y formatea la información contenida en estas páginas y serán guardadas en una colección propia, contenidas en una base de datos llamada "materiales_odontologicos" de MongoDB. para ello se ha establecido una clase Pipeline con dos métodos que se encargaran de: 

1. gestionar la conexión a la base de datos y sus colecciones
2. gestionar las opereciones CRUD que seran ejecutadas en ellas.