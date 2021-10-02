from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts import models as accountModels

def view_index(request):
	return render(request,'staffSite/index.html')

def view_listClients(request):
	clients = accountModels.Profile.objects.filter(user__is_staff=False)
	context = {'clients' : clients}
	return render(request,'staffSite/listClients.html',context)
