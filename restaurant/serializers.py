from django.db.models import Q, QuerySet
from rest_framework import serializers

from account.models import User
from account.serializers import UserSerializer
from restaurant.models import Restaurant, Modifier, Item, Category, Menu, RestaurantEmployee


class BaseSerializer(serializers.ModelSerializer):
    """
    Serializer to validate owner and employee of a restaurant
    """

    def save(self, **kwargs):
        queryset = Restaurant.objects.filter(
            Q(id=self.context['restaurant_id']) &
            (Q(owner=self.context['request'].user) |
             Q(employees__employee=self.context['request'].user))
        )

        if not queryset.exists():
            raise serializers.ValidationError({'non_field_errors': ['Invalid restaurant.']})
        return super().save(**kwargs)


class ModifierSerializer(BaseSerializer):
    def create(self, validated_data):
        validated_data['restaurant_id'] = self.context['restaurant_id']
        validated_data['item_id'] = self.context['item_id']
        return super().create(validated_data)

    class Meta:
        model = Modifier
        fields = '__all__'
        extra_kwargs = {
            'restaurant': {'read_only': True},
            'item': {'read_only': True},
            'name': {'required': True},
            'price': {'required': True},
        }


class ItemSerializer(BaseSerializer):
    modifiers = ModifierSerializer(many=True, read_only=True, source='item_modifiers')

    def create(self, validated_data):
        validated_data['category_id'] = self.context['category_id']
        validated_data['restaurant_id'] = self.context['restaurant_id']
        return super().create(validated_data)

    class Meta:
        model = Item
        fields = '__all__'
        extra_kwargs = {
            'restaurant': {'read_only': True},
            'category': {'read_only': True},
            'price': {'required': True},
            'name': {'required': True},
        }


class CategorySerializer(BaseSerializer):
    items = ItemSerializer(many=True, read_only=True, source='category_items')

    def create(self, validated_data):
        validated_data['menu_id'] = self.context['menu_id']
        validated_data['restaurant_id'] = self.context['restaurant_id']
        return super().create(validated_data)

    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs = {
            'restaurant': {'read_only': True},
            'menu': {'read_only': True},
        }


class MenuSerializer(BaseSerializer):
    categories = CategorySerializer(many=True, read_only=True, source='menu_categories')

    class Meta:
        model = Menu
        fields = '__all__'
        extra_kwargs = {
            'restaurant': {'read_only': True},
        }


class RestaurantSerializer(serializers.ModelSerializer):
    menus = MenuSerializer(many=True, read_only=True)

    def create(self, validated_data):
        # Set owner from authenticated user
        user = self.context['request'].user
        validated_data['owner'] = user
        restaurant = super().create(validated_data)

        # Update authenticated user role to owner
        user.role = User.Role.OWNER
        user.save()

        return restaurant

    class Meta:
        model = Restaurant
        fields = '__all__'
        extra_kwargs = {
            'owner': {'read_only': True},
        }


class RestaurantEmployeeSerializer(serializers.ModelSerializer):
    employee = UserSerializer()
    restaurant = RestaurantSerializer(read_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)

        # Check if restaurant is owned by authenticated user
        restaurant_id = data.get('restaurant_id')
        if not Restaurant.objects.filter(id=restaurant_id).filter(owner=self.context['request'].user).exists():
            raise serializers.ValidationError({'restaurant_id': ['Restaurant not found.']})

        return data

    class Meta:
        model = RestaurantEmployee
        fields = '__all__'
