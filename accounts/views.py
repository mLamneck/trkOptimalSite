from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from . import forms
from . import models

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('url_home')
		else:	
			return view_func(request, *args, **kwargs)

	return wrapper_func

@unauthenticated_user
def loginPage(request):
	if request.method=="POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect(request.GET.get('next', 'url_home'))
		else:
			messages.info(request, 'Username OR password isnt correct')
	context = {}
	return render(request, 'accounts/login.html', context)

def logoutPage(request):
	logout(request)
	return redirect('accounts:url_login')

@unauthenticated_user
def registerPage(request):
	form = forms.CreateUserForm()
	if request.method == "POST":
		form = forms.CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			#messages.success(request, 'Account was created for ' + user.username)
			login(request,user)
			return redirect('url_home')
	context = {'form' : form}
	return render(request, 'accounts/register.html', context)

def userProfileComplete(profile):
	return profile.complete()

@login_required()
def editProfilePage(request):
	user = request.user
	profile = models.Profile.objects.get(user=user)
	if request.method == "POST":
		userForm = forms.EditUserNameForm(request.POST,instance=user)
		form = forms.EditProfileForm(request.POST,instance=profile)
		if form.is_valid() and userForm.is_valid():
			userForm.save()
			form.save()
			return redirect('/')
	else:
		userForm = forms.EditUserNameForm(instance=user)
		form = forms.EditProfileForm(instance=profile)

	context = {'form' : form, 'userForm' : userForm}
	return render(request, 'accounts/editProfile.html', context)
