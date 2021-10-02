from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import views

app_name = 'staffSite'

urlpatterns = [
	path('', views.view_index, name='url_index'),
	path('listClients/', views.view_listClients, name='url_listClients'),	
]
