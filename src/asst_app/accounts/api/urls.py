from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='api-register'),
    path('login/', views.ObtainAuthTokenView.as_view(), name='api-login'),

    path('society/<str:pk>/', views.api_society_detail_view),
    path('society/visitors/', views.api_add_visitor_view),
    path('society/visitors/<str:name>/', views.api_visitor_detail_view),

]