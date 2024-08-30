from rest_framework.routers import DefaultRouter
from django.urls import include, path
from . import views

app_name = 'auth'

router = DefaultRouter()
router.register("sign-up", views.SignUpUserAPI, basename="sign-up")
router.register("auth", views.AuthenticationViewSet, basename="auth_views")

urlpatterns = [
    path("", include(router.urls)),
    path('login', views.LonginUserApi.as_view(), name='login'),
]