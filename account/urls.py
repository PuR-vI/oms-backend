from django.urls import path
from  account.views import UserRegistrationView,UserLoginView,UserLogoutView,UserProfileView,UserChangePasswordView

urlpatterns=[
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
]