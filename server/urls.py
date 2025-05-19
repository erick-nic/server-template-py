from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v0/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v0/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]