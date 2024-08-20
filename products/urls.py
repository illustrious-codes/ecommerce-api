from django.db import router
from rest_framework.routers import DefaultRouter
from django.urls import include, path
from . import views

app_name = "product"

router = DefaultRouter()
router.register("", views.ProductAPIView, basename="product")

urlpatterns = [
    path('', include(router.urls)),
]