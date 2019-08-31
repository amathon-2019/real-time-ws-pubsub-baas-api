from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('get_Channel/', views.get_Channel, name='Channel'),
    path('get_Server/', views.get_Server, name='Server'),
    path('update_ServerState/<str:state>/', views.update_ServerState, name='Server'),
]


