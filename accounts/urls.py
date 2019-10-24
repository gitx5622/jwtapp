from django.urls import path
from .views import api_admin_user_index, api_admin_user_detail,api_login,api_user_detail
#urls.py
urlpatterns = [
    path('user', api_admin_user_index),
    path('user/<int:pk>/', api_admin_user_detail),
    path('login/', api_login),
    path('<int:pk>/',api_user_detail),
    
]

