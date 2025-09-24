from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
   path('home', views.home, name='home'),
   path('', views.register_view, name='register'),
   path('login/', views.login_view, name='login'),
   path('activate/<str:uidb64>/<str:token>/', views.activate_account, name='activate'),
   path('password_reset/', views.password_reset_view, name='password_reset'),
   path('password_reset_confirm/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
   path('home/', views.home, name='home'),
   path('customer', include('customer.urls')),
   path('logout/', LogoutView.as_view(), name='logout'),
]
