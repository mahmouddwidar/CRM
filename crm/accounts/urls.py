from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customer/<str:primary_key>/', views.customer, name='customer'),

    path('create_order/', views.create_order, name='create_order'),
    path('update_order/<str:primary_key>', views.update_order, name='update_order'),
    path('delete_order/<str:primary_key>', views.delete_order, name='delete_order'),

    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('user/', views.userPage, name='user-page'),
    path('account/', views.accountSettings, name='account'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

'''
                   *** Bulit in Reset Views ***
1- submit email form                          //PasswordResetView.as_view()
2- Email sent success message                 //PasswordResetDoneView.as_view()
3- Link to password reset form in email       //PasswordResetConfirmView.as_view()
4- Password successfully changed message      //PasswordResetCompleteView.as_view()
'''