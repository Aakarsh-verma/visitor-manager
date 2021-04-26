from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #auth urls
    path('register/', views.register_view, name='register'),
    path('register/details/', views.regsociety, name='socdetails'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    # Password Reset urls
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='password_reset_form.html'), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),
    
    # Dashboard Urls
    path('dashboard/<str:pk>/', views.home, name='dashboard'),
    path('visitors/', views.visitors, name='visitor'),
    path('society/', views.society, name='society'),
    
    # Data comes from device
    path('enter_visitor/<str:pk>/', views.validvisitorentry, name="enter_visitor"),
    path('notenter_visitor/<str:pk>/', views.invalidvisitorentry, name="notenter_visitor")
]