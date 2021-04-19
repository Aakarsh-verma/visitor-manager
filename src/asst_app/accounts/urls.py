from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/<str:pk>/', views.home, name='dashboard'),
    path('visitors/<str:pk>/', views.visitors, name='visitor'),
    path('society/<str:pk>/', views.society, name='society'),
    path('enter_visitor/<str:pk>/', views.validvisitorentry, name="enter_visitor"),
    path('notenter_visitor/<str:pk>/', views.invalidvisitorentry, name="notenter_visitor")
]