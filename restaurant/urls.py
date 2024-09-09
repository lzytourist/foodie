from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.views import OrderViewSet
from restaurant.views import *

router = DefaultRouter()
router.register(
    r'(?P<restaurant_id>\d+)/menus',
    MenuViewSet,
    basename='menu'
)
router.register(
    r'(?P<restaurant_id>\d+)/menus/(?P<menu_id>\d+)/categories',
    CategoryViewSet,
    basename='category'
)
router.register(
    r'(?P<restaurant_id>\d+)/menus/(?P<menu_id>\d+)/categories/(?P<category_id>\d+)/items',
    ItemViewSet,
    basename='item'
)
router.register(
    r'(?P<restaurant_id>\d+)/menus/(?P<menu_id>\d+)/categories/(?P<category_id>\d+)/items/(?P<item_id>\d+)/modifiers',
    ModifierViewSet,
    basename='modifier'
)
router.register(
    r'(?P<restaurant_id>\d+)/orders',
    OrderViewSet,
    basename='order'
)

urlpatterns = [
    path('', RestaurantListCreateAPIView.as_view()),
    path('<int:pk>/', RestaurantModifyAPIView.as_view()),
    path('', include(router.urls)),
]
