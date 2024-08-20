from itertools import product
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "category",
            "description",
            "image",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate(self, data):
        price = data.get("price", "")
        if price < 0:
            raise serializers.ValidationError("Price field cannot be empty")
        return data
    
    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product