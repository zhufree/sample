#-*-coding:utf-8-*-
from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class RegistrationForm(forms.Form):
	username=forms.CharField(label='用户名',max_length=30)
	email=forms.EmailField(label='注册邮箱')
	password1=forms.CharField(label='密码',widget=forms.PasswordInput())
	password2=forms.CharField(label='确认密码',widget=forms.PasswordInput())
	def clean_password2(self):
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			password1=self.cleaned_data['password1']
			password2=self.cleaned_data['password2']
			if password1==password2:
				return password2
		raise forms.ValidationError('Passwords do not match.')
	def clean_username(self):
		username=self.cleaned_data['username']
		if not re.search(r'^\w+$',username):
			raise forms.VaildationError('Username can only contain alphanumeric characters and the underscore.')
		try:
			User.objects.get(username=username)
		except ObjectDoesNotExist:
			return username
		raise forms.ValidationError('Username is already taken.')


class MessageForm(forms.Form):
    content=forms.CharField(required=True)
class ArticleForm(forms.Form):
    title=forms.CharField(required=True)
    content=forms.CharField(required=True)
    #tag=forms.CharField(required=False)
class CommentForm(forms.Form):
    content=forms.CharField(required=True)
