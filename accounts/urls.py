from django.urls import path
from django.contrib.auth import views as auth_view
from .views import *

app_name = 'account'

urlpatterns = [
    path('login/', auth_view.LoginView.as_view(), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('detail/<int:id>/', ProfileDetail.as_view(), name='detailProfile'),
    path('subscribe/', SubscribeOrUnsibscribe.as_view(), name='subscribe'),
    path('settings/<pk>/', SettingsView.as_view(), name='settings'),
    path('newsLine/', NewsLineView.as_view(), name='NewsLine'),
    path('postIt/', PostAddView.as_view(), name='postIt'),
    path('delete/', DeletePost.as_view(), name='deletePost'),
    path('search/', SearchUserView.as_view(), name='search')
]