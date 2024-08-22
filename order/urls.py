from rest_framework.routers import DefaultRouter
from django.urls import include, path
from . import views

app_name = "order"

# router = DefaultRouter()
# router.register("", views.OrderAPIView, basename="order")


urlpatterns = [
    # path("", include(router.urls))
    path("order/<int:product_id>/product", views.OrderAPIView.as_view(), name="order")
]