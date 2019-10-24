from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('jwt/refresh-token/', refresh_jwt_token, name='refresh_jwt_token'),
    path('jwt/api-token-verify/', verify_jwt_token, name='verify_jwt_token'),
    path('jwt/api-token-auth/', obtain_jwt_token, name='obtain_jwt_token'),
    
]
