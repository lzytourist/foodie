from django.db import models

from account.models import User


class Restaurant(models.Model):
    # Foreign key of user table. User can access their restaurants using restaurants query.
    # Record is deleted when the user record is deleted from database.
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='restaurants',
    )
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True) # Date time added when the record is created
    updated_at = models.DateTimeField(auto_now=True) # Date time updated everytime the record is modified

    def __str__(self):
        return self.name

    class Meta:
        # Setting database table name
        db_table = 'restaurants'


class RestaurantEmployee(models.Model):
    """
    Store employee and restaurant combination for checking if a use is an
    employee of the restaurant.
    Provide permission checking employment status of the restaurant.
    """
    employee = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='restaurant',
    )
    restaurant = models.ForeignKey(
        to=Restaurant,
        on_delete=models.CASCADE,
        related_name='employees',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'restaurant_employees'

        # Unique employee, restaurant combination discards duplicate entries
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'restaurant'],
                name='unique_restaurant_employee',
            )
        ]


class Menu(models.Model):
    restaurant = models.ForeignKey(
        to=Restaurant,
        on_delete=models.CASCADE,
        related_name='menus',
    )
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'restaurant_menus'


class Category(models.Model):
    restaurant = models.ForeignKey(
        to=Restaurant,
        on_delete=models.CASCADE,
        related_name='restaurant_categories',
    )
    menu = models.ForeignKey(
        to=Menu,
        on_delete=models.CASCADE,
        related_name='menu_categories',
    )
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'restaurant_categories'


class Item(models.Model):
    restaurant = models.ForeignKey(
        to=Restaurant,
        on_delete=models.CASCADE,
        related_name='restaurant_items',
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='category_items',
    )
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'restaurant_items'


class Modifier(models.Model):
    restaurant = models.ForeignKey(
        to=Restaurant,
        on_delete=models.CASCADE,
        related_name='restaurant_modifiers',
    )
    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
        related_name='item_modifiers',
    )
    name = models.CharField(max_length=150)
    price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
