from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = OrderItem
    fields = [
      "id",
      "name",
      "quantity",
      "price",
    ]

class OrderSerializer(serializers.ModelSerializer):
  items = OrderItemSerializer(many=True)
  class Meta:
    model = Order
    fields = [
      "id",
      "user",
      "status",
      "created_at",
      "updated_at",
      "items",
    ]
  
  def create(self, validated_data):
    items_dict = validated_data.pop('items')
    request = self.context.get("request")
    order = Order.objects.create(user=request.user, **validated_data)
    item_obj = [
      OrderItem(
        order = order,
        name = item.get('name'),
        quantity = item.get('quantity'),
        price = item.get('price') 
      )
      for item in items_dict
    ]
    OrderItem.objects.bulk_create(item_obj)
    return order
