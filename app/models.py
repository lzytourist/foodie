from django.db import models

from account.models import User
from restaurant.models import Restaurant, Item, Modifier


class Order(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'Cash'
        CARD = 'card', 'Card'

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    total_price = models.IntegerField()
    payment_method = models.CharField(
        max_length=10,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH
    )

    class Meta:
        db_table = 'orders'


class OrderItem(models.Model):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    item = models.ForeignKey(
        to=Item,
        on_delete=models.PROTECT,
    )
    quantity = models.IntegerField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.item.name} - {self.quantity}'

    class Meta:
        db_table = 'order_items'
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'item'],
                name='unique_order_item'
            )
        ]


class OrderItemModifier(models.Model):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name='order_item_modifiers'
    )
    item = models.ForeignKey(
        to=Item,
        on_delete=models.PROTECT
    )
    modifier = models.ForeignKey(
        to=Modifier,
        on_delete=models.PROTECT
    )
    quantity = models.IntegerField()
    price = models.IntegerField()

    class Meta:
        db_table = 'order_item_modifiers'
