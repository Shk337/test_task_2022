from django.urls import include, path
from rest_framework import routers
from .views import BookViewSet

v1_router = routers.DefaultRouter()

v1_router.register(r'books', BookViewSet, basename='books')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
