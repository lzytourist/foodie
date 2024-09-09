from lib2to3.fixes.fix_input import context

from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from app.models import Order
from app.serializers import OrderSerializer
from restaurant.models import Restaurant, Menu, Category, Item, Modifier
from restaurant.permissions import IsOwner, IsOwnerOrEmployee
from restaurant.serializers import (RestaurantSerializer,
                                    MenuSerializer,
                                    CategorySerializer,
                                    ItemSerializer,
                                    ModifierSerializer)
from restaurant.utils import filter_restaurant_records


class RestaurantListCreateAPIView(ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsOwner()]
        return super().get_permissions()

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(owner=self.request.user) |
            Q(employees__employee=self.request.user)
        )


class RestaurantModifyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    queryset = Restaurant.objects.all()


class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrEmployee)

    def get_queryset(self):
        return filter_restaurant_records(
            queryset=super().get_queryset(),
            restaurant_id=self.kwargs.get('restaurant_id'),
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(restaurant_id=self.kwargs.get('restaurant_id'))


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, IsOwnerOrEmployee)

    def get_queryset(self):
        return filter_restaurant_records(
            queryset=super().get_queryset(),
            restaurant_id=self.kwargs.get('restaurant_id'),
            user=self.request.user
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['restaurant_id'] = self.kwargs.get('restaurant_id')
        context['menu_id'] = self.kwargs.get('menu_id')
        return context


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrEmployee)

    def get_queryset(self):
        return filter_restaurant_records(
            queryset=super().get_queryset(),
            restaurant_id=self.kwargs.get('restaurant_id'),
            user=self.request.user
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['restaurant_id'] = self.kwargs.get('restaurant_id')
        context['category_id'] = self.kwargs.get('category_id')
        return context


class ModifierViewSet(ModelViewSet):
    queryset = Modifier.objects.all()
    serializer_class = ModifierSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrEmployee)

    def get_queryset(self):
        return filter_restaurant_records(
            queryset=super().get_queryset(),
            restaurant_id=self.kwargs.get('restaurant_id'),
            user=self.request.user
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['restaurant_id'] = self.kwargs.get('restaurant_id')
        context['item_id'] = self.kwargs.get('item_id')
        return context


class RestaurantOrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(restaurant__owner=self.request.user) |
            Q(restaurant__employees__employee=self.request.user)
        )
