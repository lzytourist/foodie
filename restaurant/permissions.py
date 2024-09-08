from rest_framework.permissions import BasePermission

from account.models import User


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Role.OWNER

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.role != User.Role.USER

    def has_object_permission(self, request, view, obj):
        return obj.restaurant.owner == request.user or obj.restaurant.employees.filter(employee=request.user).exists()
