from django.urls import path
from . import views
urlpatterns = [
    path('', views.landing_page, name='landingpage'),

    #auth urls
    path('register/', views.register_view, name='register'),
    path('register/details/', views.regsociety, name='socdetails'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    # Dashboard Urls
    path('dashboard/<str:pk>/', views.home, name='dashboard'),
    path('visitors/', views.visitors, name='visitor'),
    path('society/', views.society, name='society'),
    
    # Data comes from raspi
    path('enter_visitor/<str:pk>/', views.validvisitorentry, name="enter_visitor"),
    path('notenter_visitor/<str:pk>/', views.invalidvisitorentry, name="notenter_visitor")
]