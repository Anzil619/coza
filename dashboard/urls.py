from django.urls import path
from . import views

urlpatterns = [
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('', views.dashboard,name='dashboard'),
    path('users/', views.users,name='users'),
    path('adminlogout/', views.adminlogout, name='adminlogout'),
    path('<int:id>/blockuser/', views.blockuser, name='blockuser'),
    # path('update/<int:user_id>', views.update,name='update'),
    # path('delete/<int:user_id>', views.delete,name='delete'),
    path('product_list/', views.product_list, name='product_list'),
    path('<int:id>/product_delete/', views.product_delete, name='product_delete'),
    path('add_product/', views.add_product, name='add_product'),
    path('product_edit/<int:product_id>/',views.product_edit,name='product_edit'),
    path('category_list/', views.category_list, name='category_list'),
    path('add_category/', views.add_category, name='add_category'),
    path('category_delete/<int:category_id>/', views.category_delete, name='category_delete'),
    path('category_edit/<int:category_id>/', views.category_edit, name='category_edit'),
    path('sub_category_list/', views.sub_category_list, name='sub_category_list'),
    path('sub_category_delete/<int:sub_id>/', views.sub_category_delete, name='sub_category_delete'),
    path('add_sub_category/', views.add_sub_category, name='add_sub_category'),
    path('sub_category_edit/<int:sub_id>/', views.sub_category_edit, name='sub_category_edit'),
    path('order_management/', views.order_management, name='order_management'),
    path('update-order/<int:id>', views.update_order, name='update_order'),
    path('coupon_management/', views.coupon_management, name='coupon_management'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path('edit_coupon/<int:coupon_id>/', views.edit_coupon, name='edit_coupon'),
    path('delete_coupon/<int:coupon_id>/', views.delete_coupon, name='delete_coupon'),
    path('variants/', views.variants, name='variants'),
    path('add_variants/', views.add_variants, name='add_variants'),
    path('edit_variants/<int:id>/', views.edit_variants, name='edit_variants'),

]
