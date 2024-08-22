from rest_framework import serializers
from yaml import serialize
from .models import Order
from products.models import Product

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id", 
            "user",
            "product",
            "quantity",
            "total_price",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "product", "total_price", "created_at", "updated_at"]

    def validate(self, data):
        product = data.get("product")
        quantity = data.get("quantity")


        if product.user == self.context.get("request").user:
            raise serializers.ValidationError("You cannot order your own product")
        if quantity is not None and quantity <= 0:
            raise serializers.ValidationError("Quantity must not be zero(0)")
        if quantity is not None and quantity > product.stock:
            raise serializers.ValidationError("Quantity exceeds the stock product")
    
        data["product"] = product
        return data