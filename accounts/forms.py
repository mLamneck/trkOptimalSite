from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *

class CreateUserForm(UserCreationForm):

	def clean_email(self):
		if User.objects.filter(email=self.cleaned_data['email']).exists():
			raise ValidationError("the given email is already registered")
		return self.cleaned_data['email']

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
