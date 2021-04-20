from django.urls import path
from . import views
urlpatterns = [
    path('', views.landing_page, name='landingpage'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.register_view, name='register'),
    path('register/details/', views.regsociety, name='socdetails'),
    path('dashboard/<str:pk>/', views.home, name='dashboard'),
    path('visitors/<str:pk>/', views.visitors, name='visitor'),
    path('society/<str:pk>/', views.society, name='society'),
    path('enter_visitor/<str:pk>/', views.validvisitorentry, name="enter_visitor"),
    path('notenter_visitor/<str:pk>/', views.invalidvisitorentry, name="notenter_visitor")
]