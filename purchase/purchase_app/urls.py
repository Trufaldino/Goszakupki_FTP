from django.urls import path
from .views import index, purchase_details, create_request, request_list, sign_up, login_view, logout_view, edit_request


app_name = 'purchase_app'

urlpatterns = [
    path('', index, name='index'),
    path('purchase_details/<int:id>/', purchase_details, name='purchase_details'),
    path('create_request/', create_request, name='create_request'),
    path('request_list/', request_list, name='request_list'),
    path('login/', login_view, name='auth_login'),
    path('logout/', logout_view, name='logout'),
    path('sign_up/', sign_up, name='sign_up'),
    path('edit_request/<int:id>/', edit_request, name='edit_request'),
]
