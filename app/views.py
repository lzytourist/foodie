from rest_framework.viewsets import ReadOnlyModelViewSet

from restaurant.models import Restaurant, Menu, Category, Item, Modifier
from restaurant.serializers import RestaurantSerializer, MenuSerializer, CategorySerializer, ItemSerializer, \
    ModifierSerializer


class RestaurantViewSet(ReadOnlyModelViewSet):
    queryset = Restaurant.objects.prefetch_related('menus').order_by('id').all()
    serializer_class = RestaurantSerializer


class RestaurantBaseViewSet(ReadOnlyModelViewSet):
    def get_queryset(self):
        return super().get_queryset().order_by('id').filter(restaurant_id=self.kwargs['restaurant_id'])


class MenuViewSet(RestaurantBaseViewSet):
    queryset = Menu.objects.prefetch_related('menu_categories').all()
    serializer_class = MenuSerializer


class CategoryViewSet(RestaurantBaseViewSet):
    queryset = Category.objects.prefetch_related('category_items').all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return super().get_queryset().filter(menu_id=self.kwargs['menu_id'])


class ItemViewSet(ReadOnlyModelViewSet):
    queryset = Item.objects.prefetch_related('item_modifiers').all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        return super().get_queryset().filter(category_id=self.kwargs['category_id'])


class ModifierViewSet(ReadOnlyModelViewSet):
    queryset = Modifier.objects.all()
    serializer_class = ModifierSerializer

    def get_queryset(self):
        return super().get_queryset().filter(item_id=self.kwargs.get('item_id'))
