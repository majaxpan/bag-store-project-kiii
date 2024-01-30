from django.contrib.admin.views.decorators import user_passes_test
from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('register/', views.userRegistration, name='register'),
    path('add_product/', user_passes_test(lambda user: user.is_superuser)(views.add_product), name='add_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
]