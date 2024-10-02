from odonto_api.app.repository.product_repository import ProductRepository


class ProductService:

    @staticmethod
    def get_by_name(nombre):
        return ProductRepository.find_by_name(nombre)

    @staticmethod
    def get_by_marca(marca):
        return ProductRepository.find_by_marca(marca)

    @staticmethod
    def get_by_categoria(categoria):
        return ProductRepository.find_by_categoria(categoria)

    @staticmethod
    def get_all():
        return ProductRepository.find_product()


