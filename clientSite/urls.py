from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import views

app_name = 'clientSite'

urlpatterns = [
	path('', views.view_index, name='url_index'),
	path('about/', views.view_about, name='url_about'),
]
