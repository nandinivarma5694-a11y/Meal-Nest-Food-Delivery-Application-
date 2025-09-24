from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path(' ',, name="home"),
    path('homee/',views.home, name="homee"),
    path('food/', views.food, name="food"),
    path('about/',views.about,name='about'),
    path('help/',views.help,name='help'),
    path('placeorder/', views.placeorder, name="placeorder"),
    path('customer-details/', views.customer_details_view, name='customer_details'),
    path('order-summary/', views.order_summary_view, name='order_summary'),
    path('search/', views.search_view, name='search'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('menu/', views.menu, name='menu'),
    path('delete/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('track-orders/', views.track_orders, name='track_orders'),
    path('cart/increase/<int:cart_item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('feedback', views.feedback, name='feedback'),

   ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
