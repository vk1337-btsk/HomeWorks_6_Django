import json
from django.core.management import BaseCommand
from django.db import connection
from catalog.models import Product, Category
from config.settings import BASE_DIR


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        """Получение данных категорий из фикстуры"""
        with open(f'{BASE_DIR}/fixtures/data_json_catalog.json', encoding='UTF-8') as file:
            data = json.load(file)
        list_category = []
        for category in data:
            if 'category' in category['model']:
                list_category.append(category)
        return list_category

    @staticmethod
    def json_read_products():
        """Получение данных продуктов из фикстуры"""
        with open(f'{BASE_DIR}/fixtures/data_json_catalog.json', encoding='UTF-8') as file:
            data = json.load(file)
        list_product = []
        for product in data:
            if 'product' in product['model']:
                list_product.append(product)
        return list_product


    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute(
                "TRUNCATE TABLE catalog_category, catalog_product RESTART IDENTITY CASCADE;")

        category_for_create = []
        product_for_create = []
        contact_for_create = []

        for category in Command.json_read_categories():
            category_for_create.append(Category(pk=category['pk'],
                                                name=category['fields']['name'],
                                                description=category['fields']['description']))

        Category.objects.bulk_create(category_for_create)

        for product in Command.json_read_products():
            product_for_create.append(Product(pk=product['pk'],
                                              name=product['fields']['name'],
                                              description=product['fields']['description'],
                                              img_product=product['fields']['image'],
                                              category=Category.objects.get(pk=product['fields']['category']),
                                              price=product['fields']['price'],
                                              created_at=product['fields']['created_at'],
                                              updated_at=product['fields']['updated_at']))

        Product.objects.bulk_create(product_for_create)
