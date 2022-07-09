from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.ProductView.as_view(), name='home') ,
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('cart/', views.add_to_cart, name='add-to-cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/', views.change_password, name='changepassword'),

    path('vegetables/', views.vegetables, name='vegetables'),
    path('vegetables/ <slug:data>', views.vegetables, name='vegetablesdata'),
    
    path('fruits/', views.fruits, name='fruits'),
    path('fruits/ <slug:data>', views.fruits, name='fruitsdata'),
    
    path('grocery/', views.grocery, name='grocery'),
    path('grocery/ <slug:data>', views.grocery, name='grocerydata'),
    
    path('dairy/', views.dairy, name='dairy'),
    path('dairy/ <slug:data>', views.dairy, name='dairydata'),
    
    path('login/', views.login, name='login'),
    path('registration/', views.customerregistration, name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
