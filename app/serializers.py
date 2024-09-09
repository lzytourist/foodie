from rest_framework import serializers

from app.models import OrderItemModifier, OrderItem, Order


class OrderItemModifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemModifier
        fields = '__all__'
        extra_kwargs = {
            'order': {'read_only': True},
            'price': {'read_only': True},
            'item': {'read_only': True},
            'order_item': {'read_only': True},
        }


class OrderItemSerializer(serializers.ModelSerializer):
    modifiers = OrderItemModifierSerializer(many=True, source='order_item_modifiers')

    class Meta:
        model = OrderItem
        fields = '__all__'
        extra_kwargs = {
            'price': {'read_only': True},
            'order': {'read_only': True},
            'modifiers': {'required': False},
        }


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, source='order_items')

    def create(self, validated_data):
        order_items = validated_data.pop('order_items')
        total_price = 0

        for order_item in order_items:
            price = order_item.get('quantity') * order_item.get('item').price
            total_price += price

            for item_modifier in order_item.get('order_item_modifiers'):
                price = item_modifier.get('quantity') * item_modifier.get('modifier').price
                total_price += price

        validated_data['total_price'] = total_price
        validated_data['user'] = self.context['request'].user

        order = super().create(validated_data)

        for order_item in order_items:
            item = OrderItem.objects.create(
                order=order,
                price=order_item.get('item').price,
                quantity=order_item.get('quantity'),
                item=order_item.get('item'),
            )

            for item_modifier in order_item.get('order_item_modifiers'):
                OrderItemModifier.objects.create(
                    order=order,
                    item=item.item,
                    price=item_modifier.get('modifier').price,
                    quantity=item_modifier.get('quantity'),
                    modifier=item_modifier.get('modifier'),
                    order_item=item
                )

        return order

    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'total_price': {'read_only': True},
            'user': {'read_only': True},
        }
