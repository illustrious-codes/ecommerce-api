from itertools import product
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets, permissions, generics
from .serializers import OrderSerializer
from .models import Order
from products.models import Product


class OrderAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_product_id(self):
        product_id = self.kwargs.get("product_id")
        product = generics.get_object_or_404(Product, id=product_id)
        return product

    def perform_create(self, serializer):
        product = self.get_product()
        return serializer.save(user=self.request.user, product=product)