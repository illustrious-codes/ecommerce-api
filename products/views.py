from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ProductSerializer
from .models import Product
from rest_framework.parsers import MultiPartParser, FormParser

class ProductAPIView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]
