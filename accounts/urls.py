from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *
router = DefaultRouter()
router.register('register', RegisterViewSet, basename='register')

urlpatterns = [
    path('register/', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('auth/me/', MeView.as_view(), name='auth-me'),
]


