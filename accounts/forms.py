from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Button
from crispy_forms.bootstrap import FormActions

from .models import *

class CreateUserForm(UserCreationForm):

	def clean_email(self):
		if User.objects.filter(email=self.cleaned_data['email']).exists():
			raise ValidationError("the given email is already registered")
		return self.cleaned_data['email']

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class EditProfileForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.fields['sleep'].placeholder = ''
		self.helper = FormHelper(self)
		#self.helper['sleep'].wrap(Field, text="hello")
		#self.helper.layout.append(Submit('save', 'save'))
		self.helper.form_tag = False
		self.helper.layout.append(
		FormActions(
			Submit('save', 'Save changes'),
			Button('cancel', 'Cancel', onclick='history.go(-1);')
			)
		)

	class Meta:
		model = Profile
		fields = '__all__'
		exclude = ['user']

class EditUserNameForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(EditUserNameForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_tag = False

	def clean_first_name(self):
		data = self.cleaned_data['first_name']
		if data == '':
			raise ValidationError("Please enter a name")
		return data

	def clean_last_name(self):
		data = self.cleaned_data['last_name']
		if data == '':
			raise ValidationError("Please enter a name")
		return data

	class Meta:
		model = User
		fields = ['first_name','last_name']

