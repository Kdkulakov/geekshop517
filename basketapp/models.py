from django.db import models

from authapp.models import User
from mainapp.models import Product
from django.utils.functional import cached_property


class BasketQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    objects = BasketQuerySet.as_manager()

    @cached_property
    def get_items_cached(self):
        return self.user.basket_set.select_related()

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    def total_quantity(self):
        _items = self.get_items_cached
        # baskets = Basket.objects.filter(user=self.user)
        map_items = map(lambda x: x.quantity, _items)
        list_items = list(map_items)
        sum_list = sum(list_items)
        return sum_list

    def total_sum(self):
        _items = self.get_items_cached
        # baskets = Basket.objects.filter(user=self.user)
        return sum(list(map(lambda x: x.product.price * x.quantity, _items)))

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    def delete(self):
       self.product.quantity += self.quantity
       self.product.save()
       super(self.__class__, self).delete()

    # переопределяем метод, сохранения объекта
    def save(self, *args, **kwargs):
        if self.pk:
            self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super(self.__class__, self).save(*args, **kwargs)