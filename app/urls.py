from rest_framework.routers import DefaultRouter

from app.views import RestaurantViewSet, MenuViewSet, CategoryViewSet, ItemViewSet, ModifierViewSet, OrderViewSet

router = DefaultRouter()
router.register(
    r'restaurants',
    RestaurantViewSet,
    basename='app-restaurant'
)
router.register(
    r'restaurants/(?P<restaurant_id>\d+)/menus',
    MenuViewSet,
    basename='app-menu'
)
router.register(
    r'restaurants/(?P<restaurant_id>\d+)/menus/(?P<menu_id>\d+)/categories',
    CategoryViewSet,
    basename='app-category'
)
router.register(
    r'restaurants/(?P<restaurant_id>\d+)/menus/(?P<menu_id>\d+)/categories/(?P<category_id>\d+)/items',
    ItemViewSet,
    basename='app-item'
)
router.register(
    r'restaurants/(?P<restaurant_id>\d+)/menus/(?P<menu_id>\d+)/categories/(?P<category_id>\d+)/items/(?P<item_id>\d+)/modifiers',
    ModifierViewSet,
    basename='app-modifier'
)
router.register(
    r'orders',
    OrderViewSet,
    basename='app-order'
)

urlpatterns = router.urls
