import datetime

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, db_column='Название категории')
    description = models.TextField(db_column='Описание')

    def __str__(self):
        return f'{self.name}: {self.description}'

    class Meta:
        db_table = "Таблица категорий"
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=100, db_column="Название")
    description = models.TextField(db_column="Описание")
    img_product = models.ImageField(upload_to='img_product/', null=True, blank=True, db_column="Картинка (превью)")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField(db_column='   Цена')
    manufactured_at = models.DateTimeField(default=datetime.datetime(1900, 12, 1, 0, 0, 0), verbose_name='Дата производства продукта')
    created_at = models.DateTimeField(auto_now_add=True, db_column='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, db_column='Дата последнего изменения')

    def __str__(self):
        return f'{self.name} - {self.price} руб.: {self.description}'

    class Meta:
        db_table = "Таблица продуктов"
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
