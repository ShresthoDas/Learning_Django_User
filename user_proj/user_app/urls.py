from django.conf.urls import url
from django.urls import path
from user_app import views

app_name = 'user_app'

urlpatterns = [path('register/',views.register, name = 'register'),
               path('login/',views.user_login, name = 'login')
]
