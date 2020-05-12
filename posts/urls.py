from django.urls import path
from .views import *

app_name = 'posts'

urlpatterns = [
     path('post/', PostDetail.as_view(), name='postDetail')
]