from django.db.models import Q


def filter_restaurant_records(queryset, restaurant_id, user):
    """
    Filter records that are connected to a restaurant.
    Restaurant is owned by the user or is an employee of the restaurant.
    """
    return queryset.filter(
        Q(restaurant_id=restaurant_id) &
        (Q(restaurant__owner=user) |
         Q(restaurant__employees__employee=user))
    )
