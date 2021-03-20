from django.urls import path

from . import views  # . represents current dir and we imported views.py file here


urlpatterns = [
    path('', views.home,name='aes-homepage'),
    path('about/',views.about,name='aes-about'),
    path('upload/',views.upload,name='aes-upload'),
    path('encrypted/',views.encrypted,name='aes-encrypted'),

]
