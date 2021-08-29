from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup, name='signup'), #회원가입
    path('login/', login_check, name='login'), #로그인
    path('logout/', logout, name='logout'), #로그아웃
]