from . import views
from django.urls import path


urlpatterns = [
    path('add_address/', views.add_address, name='add_address'),
    path('profile/', views.profile, name='profile'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('changepassword/', views.changepassword, name='changepassword'),
    

]