from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def view_index(request):
	if request.user.is_authenticated:
		print('is_authenticated')
		if request.user.profile.complete:
			print('profile complete')
		else:			
			print('profile not complete')
			return redirect('accounts:url_editProfile')
	else:
		print('is not authenticated')

	return render(request,'clientSite/index.html')

def view_about(request):
	return render(request,'clientSite/about.html')
