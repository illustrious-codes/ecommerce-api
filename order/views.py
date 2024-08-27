from itertools import product
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets, permissions, generics
from .serializers import OrderSerializer
from .models import Order
from products.models import Product
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status


class OrderAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        product_id = self.kwargs.get("product_id")
        if product_id is None:
            context['product'] = None
        else:
            try:
                product = Product.objects.get(id=product_id)
                context['product'] = product
            except Product.DoesNotExist:
                raise NotFound(detail="Product not found.")
        return context
    
    def post(self, request, *args, **kwargs):
        product = self.get_serializer_context().get('product')
        if product is None:
            return Response(
                {"detail": "Product ID is required and must be valid"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().post(request, *args, **kwargs)
