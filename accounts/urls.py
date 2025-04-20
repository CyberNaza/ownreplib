from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet
from .views import CustomTokenObtainPairView
router = DefaultRouter()
router.register('register', RegisterViewSet, basename='register')

urlpatterns = [
    path('register/', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
]


