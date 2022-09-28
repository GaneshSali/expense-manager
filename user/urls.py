
from django.urls import path
from .views import *
from django.contrib.auth import views as auth


urlpatterns = [
    path('', index, name='index'),
    path('accounts/login/', login_view, name='login'),
    path('register', register, name='register'),
    path('logout/', auth.LogoutView.as_view(template_name ='user/index.html'), name ='logout'),
    
    path('balances', BalanceList.as_view(),name='balance'),
    path('create_account', BalanceCreateView.as_view(),name='balance_create'),
    path('update_account/<int:pk>', BalanceUpdateView.as_view(),name='balance_update'),
    path('delete_account/<int:pk>', del_balance,name='balance_delete'),

    path('categories', CategoriesList.as_view(),name='categories'),
    path('create_category', CategoryCreateView.as_view(),name='category_create'),
    path('update_category/<int:pk>', CategoryUpdateView.as_view(),name='category_update'),
    path('delete_category/<int:pk>', del_category,name='category_delete'),

    path('create_data', DataCreateView.as_view(),name='data_create'),
    path('update_data/<int:pk>', DataUpdateView.as_view(),name='data_update'),
    path('delete_data/<int:pk>', del_data,name='data_delete'),

]